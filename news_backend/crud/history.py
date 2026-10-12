from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from datetime import datetime

from models.history import History
from models.news import News


async def add_news_history(
  db: AsyncSession,
  news_id: int,
  user_id: int
):
  """
  添加浏览历史记录
  """
  query = select(History).where(History.news_id == news_id, History.user_id == user_id)
  result = await db.execute(query)
  existing_history = result.scalar_one_or_none()
  if existing_history is not None:
    # 如果已经存在，则更新浏览时间
    existing_history.view_time = datetime.now()
    await db.commit()
    await db.refresh(existing_history)
    return existing_history
  else:
    # 如果不存在，则插入新的浏览历史记录
    history = History(news_id=news_id, user_id=user_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

async def get_history_list(
  db: AsyncSession,
  user_id,
  page: int = 1,
  page_size: int = 10
):
  offset = (page - 1) * page_size
  query = (
    select(News, History.view_time.label("view_time"), History.id.label("history_id"))
    .join(History, History.news_id == News.id)
    .where(History.user_id == user_id)
    .order_by(History.view_time.desc())
    .offset(offset).limit(page_size)
  )
  result = await db.execute(query)
  