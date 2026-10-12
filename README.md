# 新闻资讯 App（AI掘金头条新闻系统）

一个仿今日头条的移动端新闻浏览应用，前后端分离架构。前端基于 **Vue 3 + Vite + Vant** 构建移动端页面，后端基于 **FastAPI + SQLAlchemy（异步）** 提供 RESTful 接口，数据存储使用 **MySQL**。

支持用户注册登录、新闻分类浏览、新闻详情阅读、收藏、浏览历史、AI 问答、主题切换与多语言等能力。

---

## 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [API 接口一览](#api-接口一览)
- [数据库设计](#数据库设计)
- [认证机制](#认证机制)
- [开发脚本](#开发脚本)
- [许可证](#许可证)

---

## 技术栈

### 前端

| 类别 | 技术 | 说明 |
| --- | --- | --- |
| 框架 | Vue 3 | 组合式 API（`<script setup>`） |
| 构建工具 | Vite 7 | 开发服务器与打包 |
| UI 组件库 | Vant 4 | 移动端组件库 |
| 状态管理 | Pinia + pinia-plugin-persistedstate | 用户、主题、语言、新闻、收藏、历史等 Store |
| 路由 | Vue Router 4 | 基于 `createWebHistory` 的 SPA 路由 |
| 国际化 | Vue I18n 9 | 内置 `zh-CN` / `en-US` |
| 请求库 | Axios | 调用后端 API |
| Markdown | marked + DOMPurify | AI 回答渲染与 XSS 过滤 |

### 后端

| 类别 | 技术 | 说明 |
| --- | --- | --- |
| 语言 | Python ≥ 3.13.2 | |
| Web 框架 | FastAPI | 异步 Web 服务，自动生成 OpenAPI 文档 |
| ORM | SQLAlchemy 2.0（异步） | `AsyncSession` + `async_sessionmaker` |
| 数据库 | MySQL + aiomysql | 异步数据库驱动 |
| 密码加密 | bcrypt | 密码哈希存储 |
| 依赖/环境管理 | uv | `pyproject.toml` + `uv.lock` |
| 代码质量 | ruff / mypy / pytest | 静态检查与测试 |

---

## 项目结构

```
news/
├── news_backend/                    # 后端（FastAPI）
│   ├── config/
│   │   └── db_config.py             # 数据库引擎、异步会话、get_db 依赖
│   ├── crud/                        # 数据访问层（封装数据库操作）
│   │   ├── news.py                  # 新闻 / 分类查询、浏览量、相关推荐
│   │   ├── users.py                 # 用户、Token 的增查改
│   │   ├── favorite.py              # 收藏的增删查
│   │   └── history.py               # 浏览历史操作
│   ├── models/                      # SQLAlchemy ORM 模型
│   │   ├── news.py                  # Category / News
│   │   ├── users.py                 # User / UserToken
│   │   ├── favorite.py              # Favorite
│   │   └── history.py               # History
│   ├── routers/                     # API 路由层
│   │   ├── news.py                  # /api/news
│   │   ├── users.py                 # /api/user
│   │   ├── favorite.py              # /api/favorite
│   │   └── history.py               # /api/history
│   ├── schemas/                     # Pydantic 请求/响应模型
│   │   ├── base.py                  # NewsItemBase（公共字段）
│   │   ├── users.py                 # 用户相关模型
│   │   ├── favorite.py              # 收藏相关模型
│   │   └── history.py               # 浏览历史相关模型
│   ├── utils/                       # 工具层
│   │   ├── auth.py                  # get_current_user 认证依赖
│   │   ├── security.py              # bcrypt 密码加密/校验
│   │   ├── response.py              # 统一成功响应 success_response
│   │   ├── exception.py             # 异常处理函数
│   │   └── exception_headlers.py    # 全局异常处理器注册
│   ├── tests/
│   │   └── test_security.py         # 密码加密单元测试
│   ├── main.py                      # 应用入口（FastAPI 实例、CORS、路由挂载）
│   ├── pyproject.toml               # 依赖与项目配置
│   ├── API接口规范文档.md             # 接口详细说明
│   └── 项目后端设计说明文档.md         # 后端设计说明
│
├── news_frontend/                   # 前端（Vue 3 + Vite）
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewsItem.vue         # 新闻列表项
│   │   │   └── TabBar.vue           # 底部导航栏（首页 / AI问答 / 我的）
│   │   ├── config/
│   │   │   └── api.js               # 后端 baseURL 与 AI 问答配置
│   │   ├── i18n/
│   │   │   ├── index.js             # i18n 初始化与语言切换
│   │   │   └── locales/             # zh-CN.js / en-US.js
│   │   ├── router/
│   │   │   └── index.js             # 路由表与全局守卫
│   │   ├── store/
│   │   │   ├── index.js             # Pinia 实例与持久化插件
│   │   │   ├── user.js              # 用户状态（登录/注册/资料/密码）
│   │   │   ├── theme.js             # 主题（浅色/深色/蓝/绿）
│   │   │   ├── language.js          # 语言状态
│   │   │   └── modules/             # 业务 Store
│   │   │       ├── news.js          # 分类与新闻列表/详情
│   │   │       ├── favorite.js      # 收藏（API + 本地兜底）
│   │   │       └── history.js       # 浏览历史（API + 本地兜底）
│   │   ├── views/                   # 页面
│   │   │   ├── Home.vue             # 首页（分类 Tab + 新闻列表）
│   │   │   ├── NewsDetail.vue       # 新闻详情
│   │   │   ├── Category.vue         # 全部分类
│   │   │   ├── AIChat.vue           # AI 问答（SSE 流式）
│   │   │   ├── Favorite.vue         # 我的收藏
│   │   │   ├── History.vue          # 浏览历史
│   │   │   ├── My.vue               # 我的
│   │   │   ├── Profile.vue          # 个人信息
│   │   │   ├── Settings.vue         # 设置（主题/语言）
│   │   │   ├── Login.vue            # 登录
│   │   │   └── Register.vue         # 注册
│   │   ├── App.vue                  # 根组件（keep-alive 路由渲染）
│   │   ├── main.js                  # 应用入口（Vant/Pinia/Router/i18n 注册）
│   │   └── style.css                # 全局样式与主题变量
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── sql_data/
│   └── database.sql                 # 建库建表脚本 + 初始化数据
└── LICENSE                          # MIT
```

---

## 功能特性

### 新闻浏览
- 首页按分类（头条 / 社会 / 国内 / 国际 / 娱乐 / 体育 / 科技 / 财经）切换 Tab，支持下拉刷新与上拉加载更多。
- 全部分类页（宫格布局）一键跳转对应分类。
- 新闻详情：展示标题、作者、发布时间、浏览量、正文分段、封面图，并附带同分类「相关推荐」。
- 打开详情自动累加浏览量。

### 用户与账号
- 注册、登录，登录态通过 Pinia 持久化到 `localStorage`。
- 个人信息查看、修改个人简介、修改密码。
- 统一 Token 认证（7 天有效期）。

### 收藏与浏览历史
- 新闻详情页一键收藏 / 取消收藏（星标）。
- 收藏列表、浏览历史列表支持单条删除与一键清空。
- 已登录时走后端 API，未登录或请求失败时自动回退到本地 `localStorage`。

### AI 问答
- 独立的对话页面，支持多轮对话与 Markdown 渲染（marked + DOMPurify 防 XSS）。
- 基于阿里云 DashScope（OpenAI 兼容模式）SSE 流式输出，模型为 `qwen3-max-preview`。

### 个性化
- 主题切换：浅色 / 深色 / 蓝色 / 绿色（通过 CSS 变量动态生效）。
- 多语言：简体中文 / English（Vue I18n）。
- 移动端优先布局（最大宽度 750px，适配安全区域）。

---

## 快速开始

### 环境要求

- Python ≥ 3.13.2
- Node.js（建议 ≥ 18）
- MySQL 8.x
- [uv](https://docs.astral.sh/uv/)（后端依赖管理，可选）

### 1. 初始化数据库

在 MySQL 中执行初始化脚本（会创建 `news_app` 库、数据表及默认数据）：

```bash
mysql -u root -p < sql_data/database.sql
```

脚本会插入测试账号：用户名 `admin`，密码 `123456`。

### 2. 启动后端

```bash
cd news_backend

# 使用 uv 安装依赖并运行（推荐）
uv sync
uv run python main.py
```

或使用虚拟环境：

```bash
cd news_backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install fastapi[standard] sqlalchemy[asyncio] aiomysql bcrypt
python main.py
```

启动成功后：

- 服务地址：`http://localhost:8000`
- 交互式 API 文档：`http://localhost:8000/docs`

### 3. 启动前端

```bash
cd news_frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。开发服务器默认端口 5173，已配置在后端 CORS 白名单中。

---

## 配置说明

### 后端

数据库连接位于 [db_config.py](file:///d:/Project/VS%20code/web/news/news_backend/config/db_config.py)：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"
```

请按实际环境修改用户名、密码、主机与端口。

CORS 允许来源位于 [main.py](file:///d:/Project/VS%20code/web/news/news_backend/main.py#L12-L24)，默认仅放行 `http://localhost:5173` 与 `http://127.0.0.1:5173`。

异常处理器通过 `DEBUG_MODE` 开关控制是否返回详细堆栈（见 [exception.py](file:///d:/Project/VS%20code/web/news/news_backend/utils/exception.py#L10)），生产环境建议设为 `False`。

### 前端

API 地址与 AI 配置位于 [api.js](file:///d:/Project/VS%20code/web/news/news_frontend/src/config/api.js)：

```js
export const apiConfig = {
  baseURL: 'http://127.0.0.1:8000',   // 后端 API 基础地址
}

export const aiChatConfig = {
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  apiKey: 'API_KEY',                   // 需替换为阿里云 DashScope API Key
  model: 'qwen3-max-preview'
}
```

> 使用 AI 问答前，请在 `aiChatConfig.apiKey` 中填入有效的 DashScope API Key。

---

## API 接口一览

- 基础地址：`http://localhost:8000`
- 统一响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

- 需要认证的接口请在请求头中携带：`Authorization: Bearer <token>`

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 | 需认证 |
| --- | --- | --- | --- |
| POST | `/api/user/register` | 用户注册 | 否 |
| POST | `/api/user/login` | 用户登录 | 否 |
| GET | `/api/user/info` | 获取当前用户信息 | 是 |
| PUT | `/api/user/update` | 更新用户信息 | 是 |
| PUT | `/api/user/password` | 修改密码 | 是 |

### 新闻模块 `/api/news`

| 方法 | 路径 | 说明 | 主要参数 |
| --- | --- | --- | --- |
| GET | `/api/news/categories` | 获取新闻分类 | `skip`、`limit` |
| GET | `/api/news/list` | 获取新闻列表（分页） | `categoryId`、`page`、`pageSize` |
| GET | `/api/news/detail` | 获取新闻详情（含浏览量 +1、相关推荐） | `id` |

### 收藏模块 `/api/favorite`

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/favorite/check` | 检查收藏状态（`newsId`） |
| POST | `/api/favorite/add` | 添加收藏（`newsId`） |
| DELETE | `/api/favorite/remove` | 取消收藏（`newsId`） |
| GET | `/api/favorite/list` | 收藏列表（`page`、`pageSize`） |
| DELETE | `/api/favorite/clear` | 清空收藏 |

### 浏览历史模块 `/api/history`

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/history/add` | 添加浏览记录（`newsId`） |
| GET | `/api/history/list` | 浏览历史列表（分页） |
| DELETE | `/api/history/delete/{history_id}` | 删除单条记录 |
| DELETE | `/api/history/clear` | 清空浏览历史 |

> 收藏与浏览历史模块的接口均需认证。字段命名遵循驼峰风格（如 `newsId`、`categoryId`、`pageSize`）。
> 更完整的请求/响应示例请参考 [API接口规范文档.md](file:///d:/Project/VS%20code/web/news/news_backend/API%E6%8E%A5%E5%8F%A3%E8%A7%84%E8%8C%83%E6%96%87%E6%A1%A3.md)。

---

## 数据库设计

数据库名：`news_app`，字符集 `utf8mb4`。核心数据表：

| 表名 | 说明 |
| --- | --- |
| `user` | 用户信息（用户名、密码哈希、昵称、头像、性别、简介、手机号） |
| `user_token` | 用户令牌（令牌值、过期时间） |
| `news_category` | 新闻分类（名称、排序） |
| `news` | 新闻（标题、简介、正文、封面、作者、分类、浏览量、发布时间） |
| `related_news` | 相关新闻关联（推荐系统） |
| `favorite` | 收藏（用户 + 新闻唯一约束） |
| `history` | 浏览历史（按浏览时间倒序索引） |
| `ai_chat` | AI 聊天记录（预留） |

主要约束与索引：

- `user.username`、`user.phone` 唯一索引。
- `favorite` 对 `(user_id, news_id)` 建立唯一约束，避免重复收藏。
- `news.category_id`、`news.publish_time`、`history.view_time` 等建立查询索引。
- 关联外键统一 `ON DELETE CASCADE / ON UPDATE CASCADE`。

完整建表语句与初始化数据见 [database.sql](file:///d:/Project/VS%20code/web/news/sql_data/database.sql)。

---

## 认证机制

1. 用户登录 / 注册成功后，后端生成 `UUID` 令牌并写入 `user_token` 表，有效期 **7 天**。
2. 客户端在后续请求的 `Authorization` 头中携带令牌：`Authorization: Bearer <token>`。
3. 后端通过 `get_current_user` 依赖（见 [auth.py](file:///d:/Project/VS%20code/web/news/news_backend/utils/auth.py)）解析令牌并校验过期时间，返回对应用户。
4. 密码使用 **bcrypt** 加密存储，登录时进行校验，不保存明文。

---

## 开发脚本

### 前端（`news_frontend`）

| 命令 | 说明 |
| --- | --- |
| `npm run dev` | 启动开发服务器（默认 5173） |
| `npm run build` | 生产环境打包 |
| `npm run preview` | 本地预览打包产物 |

### 后端（`news_backend`）

| 命令 | 说明 |
| --- | --- |
| `uv sync` | 安装 / 同步依赖 |
| `uv run python main.py` | 启动服务（`reload=True`，端口 8000） |
| `uv run pytest` | 运行测试 |
| `uv run ruff check .` | 代码风格检查 |
| `uv run mypy .` | 类型检查 |

---

## 许可证

本项目基于 [MIT License](file:///d:/Project/VS%20code/web/news/LICENSE) 开源，Copyright (c) 2026 木小白。