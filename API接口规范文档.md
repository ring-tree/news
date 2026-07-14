# API 接口文档

## 概述

本文档详细描述了新闻系统的API接口，包括用户管理、新闻浏览、收藏和历史记录等功能模块。

## 基础URL

```
http://localhost:8000
```

## 认证方式

大部分接口需要认证，认证通过在请求头中添加 `Authorization` 字段实现：

```
Authorization: token值
```

## 响应格式

所有接口返回JSON格式数据，通用响应结构如下：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 接口详情

### 用户管理模块

#### 1. 用户注册

- **接口地址**: `POST /api/user/register`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

- **请求示例**:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": "example_user",
      "bio": "这个人很懒，什么都没留下",
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    }
  }
}
```

#### 2. 用户登录

- **接口地址**: `POST /api/user/login`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

- **请求示例**:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": "example_user",
      "nickname": null,
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
      "bio": "这个人很懒，什么都没留下"
    }
  }
}
```

#### 3. 获取用户信息

- **接口地址**: `GET /api/user/info`
- **请求头**: 需要认证
- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "example_user",
    "nickname": null,
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
    "gender": "unknown",
    "bio": "这个人很懒，什么都没留下"
  }
}
```

#### 4. 更新用户信息

- **接口地址**: `PUT /api/user/update`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| nickname | string | 否 | 昵称 |
| avatar | string | 否 | 头像URL |
| gender | string | 否 | 性别 |
| bio | string | 否 | 个人简介 |
| phone | string | 否 | 手机号 |

- **请求示例**:

```json
{
  "bio": "这是我的个人简介"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "username": "example_user",
    "nickname": null,
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
    "gender": "unknown",
    "bio": "这是我的个人简介"
  }
}
```

#### 5. 修改用户密码

- **接口地址**: `PUT /api/user/password`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oldPassword | string | 是 | 当前密码 |
| newPassword | string | 是 | 新密码 |

- **请求示例**:

```json
{
  "oldPassword": "current_password",
  "newPassword": "new_password"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

### 新闻模块

#### 1. 获取新闻分类列表

- **接口地址**: `GET /api/news/categories`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| skip | integer | 否 | 跳过的记录数，默认为0 |
| limit | integer | 否 | 返回的记录数限制，默认为100 |

- **请求示例**:

```
GET /api/news/categories
GET /api/news/categories?skip=0&limit=10
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-01T00:00:00",
      "name": "科技",
      "sort_order": 0
    }
  ]
}
```

#### 2. 获取新闻列表

- **接口地址**: `GET /api/news/list`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| categoryId | integer | 是 | 分类ID |
| page | integer | 否 | 页码，默认为1 |
| pageSize | integer | 否 | 每页显示的新闻数量，最大值为100，默认为10 |

- **请求示例**:

```
GET /api/news/list?categoryId=1
GET /api/news/list?categoryId=1&page=2&pageSize=20
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "publish_time": "2023-01-01T00:00:00",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "category": null,
        "title": "新闻标题",
        "description": "新闻简介",
        "content": "新闻内容",
        "image": null,
        "author": null,
        "category_id": 1,
        "views": 0
      }
    ],
    "total": 100,
    "hasMore": true
  }
}
```

#### 3. 获取新闻详情

- **接口地址**: `GET /api/news/detail`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 新闻ID |

- **请求示例**:

```
GET /api/news/detail?id=1
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "title": "新闻标题",
    "content": "新闻内容",
    "image": null,
    "author": null,
    "publishTime": "2023-01-01T00:00:00",
    "categoryId": 1,
    "views": 1,
    "relatedNews": []
  }
}
```

### 收藏模块

#### 1. 检查新闻收藏状态

- **接口地址**: `GET /api/favorite/check`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| newsId | integer | 是 | 新闻ID |

- **请求示例**:

```
GET /api/favorite/check?newsId=1
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "isFavorite": true
  }
}
```

#### 2. 添加收藏

- **接口地址**: `POST /api/favorite/add`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| newsId | integer | 是 | 新闻ID |

- **请求示例**:

```json
{
  "newsId": 1
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "收藏成功",
  "data": {
    "id": 1,
    "userId": 1,
    "newsId": 1,
    "createTime": "2023-01-01T00:00:00"
  }
}
```

#### 3. 取消收藏

- **接口地址**: `DELETE /api/favorite/remove`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| newsId | integer | 是 | 新闻ID |

- **请求示例**:

```
DELETE /api/favorite/remove?newsId=1
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "取消收藏成功",
  "data": null
}
```

#### 4. 获取收藏列表

- **接口地址**: `GET /api/favorite/list`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认为1 |
| pageSize | integer | 否 | 每页条数，默认为10，最大值为100 |

- **请求示例**:

```
GET /api/favorite/list
GET /api/favorite/list?page=1&pageSize=10
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "新闻标题",
        "description": "",
        "image": "",
        "author": "",
        "publishTime": "2023-01-01T00:00:00",
        "categoryId": 1,
        "views": 1,
        "favoriteTime": "2023-01-01T00:00:00"
      }
    ],
    "total": 1,
    "hasMore": false
  }
}
```

#### 5. 清空所有收藏

- **接口地址**: `DELETE /api/favorite/clear`
- **请求头**: 需要认证
- **响应示例**:

```json
{
  "code": 200,
  "message": "成功删除1条收藏记录",
  "data": null
}
```

### 浏览历史模块

#### 1. 添加浏览记录

- **接口地址**: `POST /api/history/add`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| newsId | integer | 是 | 新闻ID |

- **请求示例**:

```json
{
  "newsId": 1
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "添加成功",
  "data": {
    "id": 1,
    "userId": 1,
    "newsId": 1,
    "viewTime": "2023-01-01T00:00:00"
  }
}
```

#### 2. 获取浏览历史列表

- **接口地址**: `GET /api/history/list`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 页码，默认为1 |
| pageSize | integer | 否 | 每页条数，默认为10，最大值为100 |

- **请求示例**:

```
GET /api/history/list
GET /api/history/list?page=1&pageSize=10
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "新闻标题",
        "description": "",
        "image": "",
        "author": "",
        "publishTime": "2023-01-01T00:00:00",
        "categoryId": 1,
        "views": 1,
        "viewTime": "2023-01-01T00:00:00"
      }
    ],
    "total": 1,
    "hasMore": false
  }
}
```

#### 3. 删除单条浏览记录

- **接口地址**: `DELETE /api/history/delete/{history_id}`
- **请求头**: 需要认证
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| history_id | integer | 是 | 历史记录ID |

- **请求示例**:

```
DELETE /api/history/delete/1
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```

#### 4. 清空浏览历史

- **接口地址**: `DELETE /api/history/clear`
- **请求头**: 需要认证
- **响应示例**:

```json
{
  "code": 200,
  "message": "清空成功",
  "data": null
}
```