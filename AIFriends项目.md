# AIFriends项目

## lesson 1：配置环境安装包与项目设置

### 1.1 安装包：**用 Django 搭后端，用 DRF 提供 REST API，用 simplejwt 做登录鉴权，用 cors-headers 让前端能跨域调用接口。**

### 1) `django`

- Django 本体：Python 的 Web 框架
- 用来做：路由、视图、ORM（连数据库）、后台管理 admin、模板渲染等
- 简单说：后端项目的“骨架”。

### 2) `djangorestframework`（DRF）

- Django 的 REST API 框架（在 Django 上封装了一层）
- 用来做：写 API 接口更方便（序列化 serializer、权限 permission、分页 pagination、ViewSet、Router 等）
- 简单说：让你更轻松地把后端做成“前后端分离的接口服务”。

### 3) `djangorestframework-simplejwt`

- DRF 的 JWT 鉴权插件
- 用来做：登录后签发 `access token / refresh token`，前端带 token 访问受保护接口
- 简单说：实现“token 登录态”（无 session 的那种，移动端/前后端分离很常用）。

### 4) `django-cors-headers`

- 处理 **CORS 跨域** 的中间件
- 用来做：当前端（比如 `http://localhost:5173`）和后端（比如 `http://localhost:8000`）域名/端口不一样时，允许浏览器跨域请求
- 简单说：解决“浏览器拦截跨域请求”的问题。

### 1.2. 创建项目

#### 1.2.1 创建后端

1. **创建整个项目**：`django-admin startproject backend` 执行后会创建一个backend的项目目录

   目录结构如下：

   ```python
   backend/  
        manage.py        # 项目管理入口（跑服务器、迁移、创建 app 等）
        backend/
          __init__.py
          settings.py    # 配置（数据库、安装的应用、中间件、时区等）
          urls.py  	   # 路由总入口
          asgi.py
          wsgi.py        # 部署/服务端入口（WSGI/ASGI）

   ```

2.  **在项目里创建一个名为 web 的 Django 应用（app）模块**: `django-admin startapp web`

    目录结构如下：

    ```python
    web/
      __init__.py
      admin.py        # 后台管理注册模型
      apps.py         # App 配置类
      models.py       # 数据模型（ORM）
      tests.py        # 测试
      views.py        # 视图（处理请求）
      migrations/     # 数据库迁移文件
        __init__.py
    ```

    `python manage.py migrate`: 在数据库中创建/更新表结构

    即使你还没写自己的模型，Django 自带的 app（如 `auth`, `admin`, `contenttypes`, `sessions`）也需要建表，不然登录后台、用户系统等都用不了。

    `python manage.py createsuperuser`: 创建Django(admin)后台管理员账号

    `python manage.py runserver`: 启动Django开发服务器

3. **集成DRF、JWT和跨域支持**

   在`AIFriends/backend/backend/settings.py`中：

   1. 注册app 把应用和第三方库注册到 Django 项目中，让 Django 启动时会加载它们的功能。

      ```python
      INSTALLED_APPS = [  # Django 的“已安装应用列表“
          ...
          'rest_framework',  # 注册 Django REST framework
          'web',  # 注册自己创建的app(web)
          'corsheaders',  # 注册 django-cors-headers（跨域库）
      ]

      # 加入跨域中间件 把CORS 跨域处理加到 Django 的请求处理流程里
      MIDDLEWARE = [
          'corsheaders.middleware.CorsMiddleware',  # 必须尽量靠前
          ...
      ]
      ```

   2. 设置静态文件（static)和媒体文件(media, 用户上传)路径

      ```python
      # 设置静态文件(static)和媒体文件(media,用户上传)路径
      # 静态文件路径
      STATIC_URL = 'static/'
      # STATIC_ROOT = BASE_DIR / 'static'  # 生产阶段使用

      STATICFILES_DIRS = [  # 开发阶段使用，生产阶段需要注释掉
          BASE_DIR / 'static',
      ]

      # 媒体文件路径，用户上传
      MEDIA_URL = 'http://127.0.0.1:8000/media/'
      MEDIA_ROOT = BASE_DIR / 'media'
      ```

   3. 使用JWT认证：**DRF（Django REST framework）全局默认认证方式**配置,告诉 DRF 以后处理 API 请求时，默认用 **JWTAuthentication** 来识别用户身份。

      ```python
       # 使用JWT认证
         from datetime import timedelta
       
         REST_FRAMEWORK = {
             'DEFAULT_AUTHENTICATION_CLASSES': (
                 'rest_framework_simplejwt.authentication.JWTAuthentication',
             ),
         }
       
         # SimpleJWT配置
         SIMPLE_JWT = {
             'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
             'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
       
             'ROTATE_REFRESH_TOKENS': True,
             'BLACKLIST_AFTER_ROTATION': True,
       
             'AUTH_HEADER_TYPES': ('Bearer',),
         }
       
         # 配置跨域
         CORS_ALLOW_CREDENTIALS = True
       
         CORS_ALLOWED_ORIGINS = [
             "http://localhost:5173",
         ]
      ```

   4. 配置JWT接口(urls.py), 在`AIFriends/backend/web/urls.py`中：

      ```python
      from django.urls import path
         from rest_framework_simplejwt.views import (
             TokenObtainPairView,
             TokenRefreshView,
         )
       
         urlpatterns = [
             path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
             path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
         ]
      ```

      5. 配置静态文件支持

         在`AIFriends/backend/backend/urls.py`中：

         ```python
         # 仅限开发阶段使用。生产阶段需要在nginx里配置。
         if settings.DEBUG:
             urlpatterns += static(
                 '/assets/',
                 document_root=settings.BASE_DIR / 'static/frontend/assets'
             )
             urlpatterns += static(
                 '/media/',
                 document_root=settings.MEDIA_ROOT
             )
         ```

#### 1.2.2 创建前端

1. 创建项目

   在`AIFriends/`目录下执行：

   ```python
   npm create vue@latest

   # 项目名称：frontend
   # 包含的功能：Router、Pinia

   # 创建的经典文件结构
   frontend/
   ├─ index.html                 # 入口 HTML（Vite 会从这里挂载）
   ├─ package.json               # 依赖与脚本（dev/build/preview 等）
   ├─ vite.config.(js|ts)        # Vite 配置（代理/路径别名等）
   ├─ README.md
   ├─ .gitignore

   ├─ public/                    # 原样拷贝的静态资源（不经构建处理）
   │  └─ favicon.ico

   └─ src/                       # 主要源码
      ├─ main.(js|ts)            # 应用入口：createApp(App).mount('#app')
      ├─ App.vue                 # 根组件
      ├─ assets/                 # 会参与构建的资源（图片、样式等）
      │  └─ base.css / main.css
      └─ components/             # 复用组件
         └─ HelloWorld.vue
   src/ # 勾选Router
   ├─ router/
   │  └─ index.(js|ts)           # 路由表
   └─ views/                     # 页面级组件（路由页面）
      ├─ HomeView.vue
      └─ AboutView.vue

   src/  # 勾选Pinia
   └─ stores/
      └─ counter.(js|ts)         # 示例 store
       
   cd frontend
   npm install
   npm run dev
   ```

2. 设置环境变量将打包文件直接重定向到django后端: 生成的前端产物**直接输出到 Django 项目的静态目录**，这样 Django 就能把这些 JS/CSS/图片当作静态资源提供出去，实现“前后端合并部署”

   ```python
      ...
      import path from 'path'

      export default defineConfig({
        ...
        build: {
          # 打包到 Django static
          outDir: path.resolve(__dirname, '../backend/static/frontend'), 
          emptyOutDir: true,
        },
        ..
   ```

3. 合并前后端，让 Django “提供一个页面”（比如返回 Vue 的 `index.html`）Django定义一个页面需要包含下面三个文件：

   1. html 模版：`templates\index.html`

      作用：**页面长什么样，加载什么资源**

   2. views：视图/类，`templates\views\index.py`

      作用：**收到请求后，决定返回什么响应（HTML）**

      ```python
      from django.shortcuts import render

      def index(request):
          return render(request, 'index.html')
      ```

      ​

   3. urls路由：

      作用：把某个 URL 地址映射到某个 view。

#### 1.2.3 创建导航栏
   一个典型的vue文件包含以下三部分内容:
   ```
写js代码
<script setup>

</script>

写html代码
<template>

</template>

写css代码
<style scoped>

</style>



   ```