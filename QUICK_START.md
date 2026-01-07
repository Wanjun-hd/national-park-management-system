# 快速开始指南

## 项目概述

本项目是国家公园管理系统的前后端分离实现,基于您现有的数据库设计和持久层代码。

**当前状态:**
- ✅ 后端框架已搭建(Django + DRF)
- ✅ 21个数据模型已定义
- ✅ 序列化器已完成
- ✅ 前端框架已搭建(Vue 3 + Element Plus)
- ✅ API服务层已完成
- ⏳ 视图层和组件待实现

## 环境要求

### 必需软件
- **Python:** 3.9 或更高版本
- **Node.js:** 16.x 或更高版本
- **MySQL:** 8.0 或更高版本
- **Git:** 任意版本

### 推荐工具
- **IDE:** VS Code 或 PyCharm
- **API测试:** Postman 或 Insomnia
- **数据库管理:** MySQL Workbench 或 Navicat

## 第一步:数据库设置

### 1. 创建数据库并导入表结构

```bash
# 登录MySQL
mysql -u root -p

# 或者使用已有的DDL脚本
mysql -u root -p < ../DDL语句.sql
```

### 2. 导入测试数据

```bash
mysql -u root -p < ../测试数据.sql
```

### 3. 验证数据库

```sql
USE national_park_system;
SHOW TABLES;  -- 应该看到21张表
SELECT COUNT(*) FROM system_user;  -- 应该有测试用户数据
```

## 第二步:后端设置

### 1. 进入后端目录

```bash
cd national-park-web-system/backend
```

### 2. 创建Python虚拟环境

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装Python依赖

```bash
pip install -r requirements.txt
```

如果下载速度慢,可以使用国内镜像:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件,修改数据库配置
```

`.env` 文件内容示例:
```ini
DB_NAME=national_park_system
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. 测试数据库连接

```bash
python manage.py check
```

如果看到 "System check identified no issues",说明配置正确。

### 6. 启动Django开发服务器

```bash
python manage.py runserver
```

访问 http://localhost:8000/admin 查看Django管理后台。

## 第三步:前端设置

### 1. 打开新终端,进入前端目录

```bash
cd national-park-web-system/frontend
```

### 2. 安装Node.js依赖

```bash
npm install
```

如果下载速度慢,可以使用国内镜像:
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### 3. 启动Vue开发服务器

```bash
npm run dev
```

访问 http://localhost:5173 查看前端应用。

## 第四步:验证系统运行

### 1. 检查后端API

在浏览器访问:
```
http://localhost:8000/admin
```

### 2. 检查前端页面

在浏览器访问:
```
http://localhost:5173
```

## 常见问题排查

### 问题1: Python依赖安装失败

**解决方案:**
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题2: MySQL连接失败

**检查清单:**
1. MySQL服务是否启动
2. .env文件中的密码是否正确
3. 数据库名称是否存在
4. 用户是否有访问权限

**测试连接:**
```bash
mysql -u root -p -e "SELECT 1"
```

### 问题3: PyMySQL导入错误

**解决方案:**
确保在 `national_park/__init__.py` 中有:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 问题4: 前端npm install失败

**解决方案:**
```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules和package-lock.json
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 问题5: CORS跨域错误

**检查后端设置:**
确保 `settings.py` 中有:
```python
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

## 下一步开发

### 后端开发任务

1. **实现API Views**
   - 创建 `backend/api/views.py`
   - 为每个业务线创建ViewSet
   - 参考现有的DAO代码实现业务逻辑

2. **配置URL路由**
   - 创建 `backend/api/urls.py`
   - 注册路由

3. **实现权限控制**
   - 创建 `backend/api/permissions.py`
   - 基于用户角色控制访问

### 前端开发任务

1. **实现登录页面**
   - 创建 `frontend/src/views/Login.vue`
   - 实现登录表单
   - 集成认证API

2. **实现主布局**
   - 创建 `frontend/src/layouts/MainLayout.vue`
   - 实现Header、Sidebar组件

3. **实现业务页面**
   - 按模块实现20+页面
   - 使用Element Plus组件库
   - 集成ECharts图表

## 推荐开发流程

### 第一阶段:核心功能(第1-2天)
1. 实现用户登录认证
2. 实现主布局和导航
3. 实现仪表盘

### 第二阶段:业务模块(第3-5天)
1. 实现生物多样性监测模块
2. 实现环境监测模块
3. 实现游客管理模块

### 第三阶段:完善功能(第6-7天)
1. 实现执法监管模块
2. 实现科研支撑模块
3. 实现系统管理模块

### 第四阶段:优化测试(第8-10天)
1. 性能优化
2. 单元测试
3. 集成测试
4. 用户体验优化

## 开发工具推荐

### VS Code插件
- **Python:** Python, Pylance
- **Vue:** Volar, Vue VSCode Snippets
- **其他:** ESLint, Prettier, GitLens

### Chrome插件
- **Vue Devtools:** 调试Vue应用
- **JSON Formatter:** 格式化API响应

## 学习资源

### Django相关
- Django官方文档: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django教程(中文): https://www.runoob.com/django/

### Vue相关
- Vue 3官方文档: https://cn.vuejs.org/
- Element Plus文档: https://element-plus.org/zh-CN/
- Pinia文档: https://pinia.vuejs.org/zh/

### 其他资源
- ECharts文档: https://echarts.apache.org/zh/
- Axios文档: https://axios-http.com/zh/

## 获取帮助

如果遇到问题:
1. 查看项目README.md和PROJECT_STRUCTURE.md
2. 检查控制台错误信息
3. 查阅官方文档
4. 在开发者社区提问

---

**祝您开发顺利!** 🚀
