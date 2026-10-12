from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UniqueConstraint, Index, Integer, DateTime, ForeignKey

from models.users import User
from models.news import News

class Base(DeclarativeBase):
  pass

class History(Base):
  """
  浏览器历史表ORM模型
  """
  __tablename__ = "history"

  # 配置索引与唯一约束
  __table_args__ = (
    Index("fk_history_user_idx", "user_id"),
    Index("fk_history_news_idx", "news_id"),
    Index("idx_view_time", "view_time", mysql_order="DESC")
  )

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史ID")
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="用户ID")
  news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False, comment="新闻ID")
  view_time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, comment="浏览时间")

  def __repr__(self):
    return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"