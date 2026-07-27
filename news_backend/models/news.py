from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Index, Text, ForeignKey

class Base(DeclarativeBase):
  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    comment="创建时间"
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now,
    onupdate=datetime.now,
    comment="更新时间"
  )

# 创建模型类
# 分类数据模型类
class Category(Base):
  __tablename__ = "news_category"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
  sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

  def __repr__(self):
    return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"

# 新闻数据模型类
class News(Base):
    __tablename__ = "news"

    # 索引配置：提升查询速度
    __table_args__ = (
      Index('fk_news_category_idx', 'category_id'),
      Index('idx_publish_time', 'publish_time'),
    )

    # --- 字段定义 ---
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    # --- 辅助方法 ---
    def __repr__(self):
      return f"<News(id={self.id}, title='{self.title}', views={self.views})>"