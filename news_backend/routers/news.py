from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# 创建 APIRouter 实例
# prefix: 设置路由前缀（API 接口规范文档）
# tags: 设置路由标签
router = APIRouter(prefix="/api/news", tags=["news"])

# 接口实现流程
# 1. 模块化路由 -> API 接口规范文档
# 2. 定义模型类 -> 数据库表（数据库设计文档）
# 3. 在 crud 文件夹里面创建文件，封装操作数据库方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

from fastapi.params import Query

from crud import news
from config.db_config import get_db
@router.get("/categories")
async def get_categories(
  skip: int = Query(default=0, ge=0, description="起始页码"),
  limit: int = Query(default=10, ge=0, description="每页显示数量"),
  db: AsyncSession = Depends(get_db)
):
  # 先获取数据库里面的新闻分类数据 -> 先定义模型类 -> 封装查询数据的方法
  categories = await news.get_categories(db, skip, limit)
  return {
    "code": 200,
    "message": "获取新闻分类成功",
    "data": categories
  }

@router.get("/list")
async def get_news_list(
  category_id: int = Query(..., ge=1, le=8, alias="categoryId"),
  page: int = 1,
  page_size: int = Query(10, alias="pageSize", le=100),
  db: AsyncSession = Depends(get_db)
):
  #思路：处理分页规则 -> 查询新闻列表 -> 计算总量 -> 计算是否还有更多

  offset = (page - 1) * page_size
  news_list = await news.get_news_list(db, category_id, offset, page_size)

  total = await news.get_news_count(db, category_id)

  hasMore = (offset + len(news_list)) < total
  return {
    "code": 200,
    "message": "获取新闻列表成功",
    "data": {
      "list": news_list,
      "total": total,
      "hasMore": hasMore
    }
  }

@router.get("/detail")
async def get_news_detail(
  news_id: int = Query(..., alias="id"),
  db: AsyncSession = Depends(get_db)
):
  # 获取新闻详情 + 浏览量+1 + 相关新闻
  news_detail = await news.get_news_detail(db, news_id)
  if not news_detail:
    raise HTTPException(status_code=404, detail="新闻不存在")

  views_res = await news.increase_news_views(db, news_detail.id)
  if not views_res:
    raise HTTPException(status_code=404, detail="新闻不存在")

  related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id)

  return {
    "code": 200,
    "message": "success",
    "data": {
      "id": news_detail.id,
      "title": news_detail.title,
      "content": news_detail.content,
      "image": news_detail.image,
      "author": news_detail.author,
      "publishTime": news_detail.publish_time,
      "categoryId": news_detail.category_id,
      "views": news_detail.views,
      "relatedNews": related_news
    }
  }