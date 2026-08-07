from datetime import datetime
from typing import Optional

from sqlalchemy import Index, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  pass


class User(Base):
  """
  用户信息表ORM模型
  """
  __tablename__ = 'user'

  # 创建索引
  __table_args__ = (
    Index('username_UNIQUE', 'username'),
    Index('phone_UNIQUE', 'phone'),
  )

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码')
  nickname: Mapped[Optional[str]] = mapped_column(String(50), comment='昵称')
  avatar: Mapped[Optional[str]] = mapped_column(String(255), comment='头像URL', default='https://fastly.jsdelivr...')
  gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'))
  bio: Mapped[Optional[str]] = mapped_column(String(500), comment='个人简介', default='')
  phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment='手机号')
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment='更新时间')

  def __repr__(self):
    return f'<User(id={self.id}, username=\'{self.username}\', nickname=\'{self.nickname}\')>'

class UserToken(Base):
  """
  用户令牌表ORM模型
  """
  __tablename__ = 'user_token'

  # 创建索引
  __table_args__ = (
    Index('token_UNIQUE', 'token'),
    Index('fk_user_token_user_idx', 'user_id'),
  )

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="用户ID")
  token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
  expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")

  def __repr__(self):
    return f"<UserToken(id={self.id}, user_id={self.user_id}, token='{self.token}')>"