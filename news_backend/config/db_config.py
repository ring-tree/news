from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 数据库 URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
  ASYNC_DATABASE_URL,
  echo=True,  # 输出 SQL 日志
  pool_size=10,  # 设置连接池中保持的持久连接数
  max_overflow=20  # 设置连接池中允许的最大溢出连接数
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
  bind=async_engine,
  class_=AsyncSession,
  expire_on_commit=False  # 禁用过期检查，避免在提交后访问已过期的对象
)

# 依赖项，用于获取数据库会话
async def get_db():
  async with AsyncSessionLocal() as session:
    try:
      yield session
      await session.commit()  # 提交事务
    except Exception as e:
      await session.rollback()  # 回滚事务
      raise e
    finally:
      await session.close()