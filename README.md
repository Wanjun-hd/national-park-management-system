# 🏔️ 国家公园管理系统

> 基于 **Django + Vue 3** 的前后端分离国家公园综合管理平台

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.3.4-blue.svg)](https://vuejs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-学习项目-red.svg)]()

## 📖 项目简介

本系统是一个功能完善的国家公园综合管理平台，涵盖**生物多样性监测、环境监测、游客管理、执法监管和科研支撑**五大业务模块，支持 8 种用户角色，21个数据表，44个索引，20个视图。

### ✨ 核心特性

- 🎨 **现代化 UI 设计** - 采用 Element Plus + 渐变色设计
- 🔐 **完善的权限系统** - RBAC权限控制 + JWT认证
- 📡 **RESTful API** - 标准化的API设计
- 📊 **数据可视化** - 实时统计仪表盘
- 📱 **响应式布局** - 支持多设备访问
- 📚 **API文档** - Swagger UI + ReDoc自动生成

## 🛠️ 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Django | 4.2.7 | Web框架 |
| Django REST Framework | 3.14.0 | REST API框架 |
| MySQL | 8.0+ | 关系型数据库 |
| JWT | 5.3.0 | Token认证 |
| drf-spectacular | 0.27.0 | API文档生成 |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.3.4 | 前端框架 |
| Element Plus | 2.4.4 | UI组件库 |
| Pinia | 2.1.7 | 状态管理 |
| Vue Router | 4.2.5 | 路由管理 |
| Axios | 1.6.2 | HTTP客户端 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0+

### 1️⃣ 数据库准备

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE national_park_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入DDL
USE national_park_system;
SOURCE path/to/your/ddl.sql;
```

### 2️⃣ 后端启动

**Windows 快速启动（推荐）**:
```bash
cd backend
双击 start.bat
```

**手动启动**:
```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Linux/Mac: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env
# 编辑 .env 文件配置数据库

# 启动服务器
python manage.py runserver
```

✅ 后端服务: http://127.0.0.1:8000
📚 API文档: http://127.0.0.1:8000/api/docs/

### 3️⃣ 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

✅ 前端应用: http://localhost:5173

### 4️⃣ 创建测试账号

访问登录页面，点击"创建测试账号"按钮，系统将自动创建以下账号：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 系统管理员 |
| monitor | monitor123 | 生态监测员 |

## 📋 功能模块

### 1. 🔐 用户认证

- [x] JWT Token 认证
- [x] 用户登录/登出
- [x] SHA-256 密码加密
- [x] 账号锁定机制（5次失败）
- [x] 8种用户角色权限

### 2. 🌿 生物多样性监测

- [x] 物种信息管理（CRUD）
- [x] 栖息地管理
- [x] 监测设备管理
- [x] 监测记录管理
- [x] 受保护物种统计
- [x] 物种数据分析

### 3. 🌍 环境监测

- [x] 监测指标管理
- [x] 环境数据采集
- [x] 数据质量控制
- [x] 环境数据统计分析
- [x] 多维度数据查询

### 4. 👥 游客管理

- [x] 游客信息管理
- [x] 在线预约系统
- [x] 预约取消功能
- [x] 流量控制管理
- [x] 流量统计分析

### 5. ⚖️ 执法监管

- [x] 违法行为记录
- [x] 执法调度管理
- [x] 案件处理流程
- [x] 执法统计分析

### 6. 🔬 科研支撑

- [x] 科研项目管理
- [x] 科研数据采集
- [x] 科研成果管理
- [x] 数据访问权限控制

### 7. 📊 统计分析

- [x] 综合仪表盘
- [x] 实时数据统计
- [x] 各模块数据概览
- [x] 可视化展示

## 🎯 项目亮点

### 后端亮点

#### 1. 完善的权限系统（`api/permissions.py`）
```python
✅ 12个自定义权限类
✅ 8种用户角色
✅ 对象级权限控制
✅ 灵活的权限组合
```

#### 2. 全面的数据验证（`api/validators.py`）
```python
✅ 19个验证器函数
✅ 3个业务验证类
✅ 手机号、身份证验证
✅ 地理坐标验证
✅ 业务数据验证
```

#### 3. 统一异常处理（`api/exceptions.py`）
```python
✅ 15个业务异常类
✅ 标准化错误响应
✅ 友好错误提示
✅ 详细错误日志
```

#### 4. 丰富工具库（`api/utils.py`）
```python
✅ 20+ 工具函数
✅ 数据导出/脱敏
✅ 统计分析辅助
✅ 距离计算
✅ 报告生成
```

#### 5. API文档自动生成
- **Swagger UI**: 交互式API测试
- **ReDoc**: 美观的文档界面
- **OpenAPI 3.0**: 标准规范

### 前端亮点

#### 1. 现代化UI设计
- ✨ 渐变色卡片设计
- 🎨 流畅的动画效果
- 📱 完全响应式布局
- 🖼️ 精美的国家公园背景

#### 2. 完整的仪表盘
- 📊 实时统计数据
- 📈 5大业务模块概览
- 🔄 自动数据刷新
- 🎯 关键指标展示

#### 3. 状态管理
- 💾 Pinia状态管理
- 🔄 Token自动刷新
- 💾 用户信息持久化

## 📁 项目结构

```
national-park-web-system/
├── backend/                    # 后端服务 🔧
│   ├── api/                   # API应用
│   │   ├── models.py         # 21个数据模型
│   │   ├── serializers.py    # DRF序列化器
│   │   ├── views.py          # 13个ViewSet + API视图
│   │   ├── urls.py           # API路由配置
│   │   ├── permissions.py    # 12个权限类 🔐
│   │   ├── validators.py     # 19个验证器 ✅
│   │   ├── exceptions.py     # 15个异常类 🚨
│   │   └── utils.py          # 20+工具函数 🛠️
│   ├── national_park/        # 项目配置
│   ├── logs/                 # 日志目录
│   ├── start.bat             # Windows启动脚本
│   ├── .env.example          # 环境变量模板
│   ├── requirements.txt      # Python依赖
│   ├── README.md             # 后端文档（600+行）
│   ├── IMPROVEMENTS.md       # 改进总结
│   └── API_REFERENCE.md      # API参考手册（400+行）
│
├── frontend/                  # 前端应用 🎨
│   ├── src/
│   │   ├── views/            # 页面组件
│   │   │   ├── Login.vue    # 精美登录页
│   │   │   ├── Dashboard.vue # 功能完整的仪表盘
│   │   │   └── ...           # 业务页面
│   │   ├── layouts/          # 布局组件
│   │   ├── store/            # Pinia状态
│   │   ├── router/           # 路由配置
│   │   ├── api/              # API接口
│   │   └── utils/            # 工具函数
│   └── package.json          # Node依赖
│
├── README.md                  # 项目总览（本文件）
└── [文档...]                  # 其他文档
```

## 💻 API 参考

### 认证相关

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/auth/login/` | 用户登录 |
| POST | `/api/auth/create-test-user/` | 创建测试用户 |
| POST | `/api/token/refresh/` | 刷新Token |

### 业务接口

| 模块 | 端点前缀 | 说明 |
|------|----------|------|
| 生物多样性 | `/api/biodiversity/` | 物种、栖息地、监测 |
| 环境监测 | `/api/environment/` | 环境数据、指标 |
| 游客管理 | `/api/visitor/` | 游客、预约、流量 |
| 执法监管 | `/api/enforcement/` | 违法行为、调度 |
| 科研支撑 | `/api/research/` | 项目、数据、成果 |
| 统计分析 | `/api/dashboard/stats/` | 综合统计数据 |

**完整API文档**: http://127.0.0.1:8000/api/docs/

## 🗄️ 数据库设计

### 核心数据表（21张）

| 类别 | 表名 | 说明 |
|------|------|------|
| 用户 | system_user | 系统用户 |
| 生物 | species, habitat | 物种、栖息地 |
| 生物 | monitoring_device, monitoring_record | 监测设备、记录 |
| 环境 | monitoring_indicator, environmental_data | 指标、数据 |
| 游客 | visitor, reservation, traffic_control | 游客、预约、流量 |
| 执法 | illegal_behavior, enforcement_dispatch | 违法、调度 |
| 科研 | research_project, research_data_collection | 项目、采集 |
| 科研 | research_achievement | 成果 |
| 基础 | functional_area | 功能分区 |

### 数据库优化

- ✅ **44个索引** - 查询性能优化
- ✅ **20个视图** - 简化复杂查询
- ✅ **存储过程** - 业务逻辑封装

## 🔒 安全特性

| 特性 | 实现 |
|------|------|
| 密码加密 | SHA-256哈希 |
| 身份认证 | JWT Token |
| 账号保护 | 5次失败锁定 |
| 权限控制 | RBAC + 对象级权限 |
| 数据验证 | 19个验证器 |
| SQL注入 | Django ORM防护 |
| XSS防护 | DRF自动转义 |
| CSRF | Django内置保护 |

## 📖 使用指南

### 登录系统

1. 启动后端和前端服务
2. 访问 http://localhost:5173
3. 点击"创建测试账号"
4. 使用 `admin` / `admin123` 登录

### 查看仪表盘

登录后自动跳转到仪表盘，显示：
- 📊 物种、设备、游客、项目统计
- 📈 五大业务模块数据概览
- ⚙️ 系统运行状态

### 测试API

访问 http://127.0.0.1:8000/api/docs/ 使用 Swagger UI 测试所有API

## 🎓 开发者指南

### 添加新的API端点

1. 在 `api/models.py` 定义模型
2. 在 `api/serializers.py` 创建序列化器
3. 在 `api/views.py` 创建ViewSet
4. 在 `api/urls.py` 注册路由
5. API文档自动更新 ✨

### 添加新的前端页面

1. 在 `frontend/src/views/` 创建组件
2. 在 `frontend/src/router/index.js` 添加路由
3. 在菜单中添加入口

## 📈 开发进度

### ✅ 已完成

#### 后端（100%）
- ✅ Django项目结构
- ✅ 21个数据模型
- ✅ DRF序列化器
- ✅ 13个ViewSet + API视图
- ✅ JWT认证系统
- ✅ 权限控制系统（12个类）
- ✅ 数据验证系统（19个验证器）
- ✅ 异常处理系统（15个异常类）
- ✅ 工具函数库（20+函数）
- ✅ API文档自动生成
- ✅ 完整的文档（1000+行）

#### 前端（80%）
- ✅ Vue项目结构
- ✅ 路由配置 + 权限守卫
- ✅ Pinia状态管理
- ✅ API服务层
- ✅ 登录页面（精美UI）
- ✅ 仪表盘页面（功能完整）
- ✅ 主布局组件
- ⏳ 业务页面组件（20+ 待完善）

### 🔄 待完善

- ⏳ 完整的业务页面（物种管理、环境数据等）
- ⏳ 数据可视化图表（ECharts）
- ⏳ 文件上传功能
- ⏳ 单元测试
- ⏳ 性能优化

## 📦 部署指南

### 开发环境

```bash
# 后端
cd backend && python manage.py runserver

# 前端
cd frontend && npm run dev
```

### 生产环境

```bash
# 后端
cd backend
gunicorn national_park.wsgi:application --bind 0.0.0.0:8000

# 前端
cd frontend
npm run build
# 部署 dist/ 到 Nginx
```

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        root /path/to/frontend/dist;
        try_files $uri /index.html;
    }

    # 后端API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    # 静态文件
    location /static/ {
        alias /path/to/backend/staticfiles/;
    }
}
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### Version 1.0.0 (2025-12-30)

**🎉 首次发布**

**后端功能**:
- ✅ 完整的 REST API
- ✅ JWT 认证系统
- ✅ 权限控制系统（12个权限类）
- ✅ 数据验证系统（19个验证器）
- ✅ 异常处理系统（15个异常类）
- ✅ 工具函数库（20+函数）
- ✅ API 文档自动生成

**前端功能**:
- ✅ 精美的登录界面
- ✅ 功能完整的仪表盘
- ✅ 路由守卫
- ✅ 状态管理
- ✅ 响应式布局

## 📄 许可证

本项目仅供学习和研究使用。

## 📞 联系方式

如有问题，请提交 Issue 或联系项目维护者。

---

<div align="center">

**🏔️ 守护自然 · 传承文明 · 科技赋能 🏔️**

Made with ❤️ by 国家公园管理系统开发组

**版本**: 1.0.0 | **最后更新**: 2025-12-30

[📚 后端文档](backend/README.md) · [📖 API参考](backend/API_REFERENCE.md) · [🔧 改进总结](backend/IMPROVEMENTS.md)

</div>
