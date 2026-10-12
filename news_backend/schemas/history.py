from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
  """
  添加浏览历史的请求模型
  """
  news_id: int = Field(..., alias="newsId")

class HistoryItemResponse(NewsItemBase):
  """
  浏览历史单挑数据的响应模型
  """
  history_id: int = Field(..., alias="historyId")
  view_time: datetime = Field(..., alias="viewTime")

  model_config = ConfigDict(
    populate_by_name=True,    # 允许同时使用 Python 字段名和 alias 进行赋值
    from_attributes=True      # 允许直接从 SQLAlchemy ORM 对象转换
  )

class HistoryListResponse(BaseModel):
  """
  浏览历史列表的响应模型
  """
  list: list[HistoryItemResponse]
  total: int
  has_more: bool = Field(..., alias="hasMore")

  model_config = ConfigDict(
    populate_by_name=True,
    from_attributes=True
  )