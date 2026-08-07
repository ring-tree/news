# 整合 根据 Token 查询用户，返回用户
from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users


async def get_current_user(
  authorization: str = Header(..., alias="Authorization"),
  db: AsyncSession = Depends(get_db)
):
  try:
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="授权头格式无效，请检查 " + f"authorization: {authorization}",
        )
    token = parts[1]
  except AttributeError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="授权头丢失或无效，请检查 " + f"authorization: {authorization}",
    )
  user = await users.get_user_by_token(db, token)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="无效的令牌或已经过期的令牌"
    )
  return user