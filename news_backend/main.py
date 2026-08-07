import uvicorn
from fastapi import FastAPI

app = FastAPI()

# 注册异常处理器
from utils.exception_headlers import register_exception_handlers
register_exception_handlers(app)

# 跨域资源共享
from fastapi.middleware.cors import CORSMiddleware
# 允许的源列表
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # 允许的跨域来源
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],     # 允许所有方法
    allow_headers=["*"]      # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "hello news"}


# 挂载/注册路由
from routers import news, users
app.include_router(news.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)