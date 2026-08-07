from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, update
from schemas.users import UserRequest, UserUpdateRequest
import uuid

from models.users import User, UserToken
from utils import security


# 根据用户名查询数据库
async def get_user_by_username(
  db: AsyncSession,
  username: str
):
  query = select(User).where(User.username == username)
  result = await db.execute(query)
  return result.scalar_one_or_none()

# 创建用户
async def create_user(
  db: AsyncSession,
  user_data: UserRequest
):
  # 先密码加密处理 -> add
  hashed_password = security.get_hash_password(user_data.password)
  user = User(username=user_data.username, password=hashed_password)
  db.add(user)
  await db.commit()
  await db.refresh(user)  # 从数据库读回最新的 user
  return user


# 生成 Token
async def create_token(
  db: AsyncSession,
  user_id: int
):
  # 生成 Token + 设置过期时间 -> 查询数据库当前用户是否有 Token -> 有：更新 没有：添加
  token = str(uuid.uuid4())
  expires_at = datetime.now() + timedelta(days=7)
  query = select(UserToken).where(UserToken.user_id == user_id)
  result = await db.execute(query)
  user_token = result.scalar_one_or_none()

  if user_token:
    user_token.token = token
    user_token.expires_at = expires_at
  else:
    user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(user_token)
    await db.commit()

  return token

async def authenticate_user(
  db: AsyncSession,
  username: str,
  password: str
):
  user = await get_user_by_username(db, username);
  if not user:
    return None
  if not security.verify_password(password, user.password):
    return None

  return user

# 根据 Token 查询用户：验证 Token -> 查询用户
async def get_user_by_token(
  db: AsyncSession,
  token: str
):
  query = select(UserToken).where(UserToken.token == token)
  result = await db.execute(query)
  user_token = result.scalar_one_or_none()
  if not user_token or user_token.expires_at < datetime.now():
    return None

  query = select(User).where(User.id == user_token.user_id)
  result = await db.execute(query)
  return result.scalar_one_or_none()


# 更新用户信息：update 更新 -> 检查是否命中 -> 获取更新后的用户返回
async def update_user(
  db: AsyncSession,
  username: str,
  user_data: UserUpdateRequest
):
  # user_data 是一个 Pydantic 模型类，需要得到数据字典，user_data.model_dump() -> ** 解包
  # 没有设置值的字段，则不会更新
  query = update(User).where(User.username == username).values(**user_data.model_dump(
    exclude_unset=True,
    exclude_none=True
  ))
  result = await db.execute(query)

  # 检查更新
  if result.rowcount == 0:
    raise HTTPException(status_code=404, detail="用户不存在")

  # 获取更新后的用户
  update_user = await get_user_by_username(db, username)
  return update_user


# 修改密码：验证旧密码 -> 新密码加密 -> 修改密码
async def change_password(
  old_password: str,
  new_password: str,
  user: User,
  db: AsyncSession
):
  if not security.verify_password(old_password, user.password):
    return False

  hashed_nwe_pwd = security.get_hash_password(new_password)
  user.password = hashed_nwe_pwd
  # 更新：由 SQLAlchemy 创建的 ORM 对象，会自动将数据更新到数据库，确保可以 commit
  # 规避 session 过期或关闭导致的不能提交的问题
  db.add(user)
  await db.commit()
  await db.refresh(user)
  return True