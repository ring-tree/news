from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import history
from schemas.history import HistoryAddRequest
from schemas.users import User
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
  data: HistoryAddRequest,
  user: User = Depends(get_current_user),
  db: AsyncSession = Depends(get_db)
):
  """
  添加浏览历史记录
  """
  result = await history.add_news_history(db, data.news_id, user.id)
  return success_response(message="添加历史记录成功", data=result)

@router.get("/list")
async def get_history_list(
  page: int = Query(1, ge=10),
  page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
  user: User = Depends(get_current_user),
  db: AsyncSession = Depends(get_db)
):
  return success_response(message="获取历史记录列表成功")