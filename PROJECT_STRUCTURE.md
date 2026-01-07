# 项目结构详细说明

## 完整目录树

```
national-park-web-system/
│
├── README.md                                    # 项目说明文档
├── PROJECT_STRUCTURE.md                         # 本文件 - 结构说明
│
├── backend/                                     # Django后端目录
│   ├── manage.py                               # Django管理命令
│   ├── requirements.txt                        # Python依赖列表
│   ├── .env.example                            # 环境变量模板
│   │
│   ├── national_park/                          # Django项目配置
│   │   ├── __init__.py                        # PyMySQL配置
│   │   ├── settings.py                         # 项目设置(数据库、中间件、CORS等)
│   │   ├── urls.py                             # 主URL配置
│   │   ├── wsgi.py                             # WSGI部署接口
│   │   └── asgi.py                             # ASGI部署接口
│   │
│   ├── api/                                    # API应用目录
│   │   ├── __init__.py
│   │   ├── apps.py                             # 应用配置
│   │   ├── models.py                           # 21个Django模型(managed=False)
│   │   ├── serializers.py                      # DRF序列化器(按5条业务线组织)
│   │   ├── admin.py                            # Django Admin配置
│   │   ├── views.py                            # API视图(待实现)
│   │   ├── urls.py                             # API路由(待实现)
│   │   ├── permissions.py                      # 权限类(待实现)
│   │   └── utils.py                            # 工具函数(待实现)
│   │
│   └── logs/                                   # 日志目录(自动创建)
│
└── frontend/                                    # Vue前端目录
    ├── package.json                            # NPM依赖
    ├── vite.config.js                          # Vite打包配置
    ├── index.html                              # HTML入口
    │
    ├── public/                                 # 静态资源(待添加)
    │   └── favicon.ico
    │
    └── src/                                    # 源代码目录
        ├── main.js                             # Vue应用入口
        ├── App.vue                             # 根组件
        │
        ├── router/                             # 路由配置
        │   └── index.js                        # Vue Router + 权限守卫
        │
        ├── store/                              # 状态管理
        │   └── auth.js                         # 认证状态(Pinia)
        │
        ├── api/                                # API服务层
        │   ├── auth.js                         # 认证API
        │   ├── biodiversity.js                 # 生物多样性API
        │   ├── environment.js                  # 环境监测API
        │   ├── visitor.js                      # 游客管理API
        │   ├── enforcement.js                  # 执法监管API
        │   └── research.js                     # 科研支撑API
        │
        ├── utils/                              # 工具函数
        │   └── request.js                      # Axios封装 + 拦截器
        │
        ├── views/                              # 页面视图(待实现)
        │   ├── Login.vue                       # 登录页
        │   ├── Dashboard.vue                   # 仪表盘
        │   ├── NotFound.vue                    # 404页面
        │   ├── biodiversity/                   # 生物多样性模块
        │   │   ├── SpeciesManagement.vue
        │   │   ├── HabitatManagement.vue
        │   │   └── MonitoringRecord.vue
        │   ├── environment/                    # 环境监测模块
        │   │   ├── DeviceManagement.vue
        │   │   ├── EnvironmentalData.vue
        │   │   └── IndicatorManagement.vue
        │   ├── visitor/                        # 游客管理模块
        │   │   ├── VisitorList.vue
        │   │   ├── ReservationManagement.vue
        │   │   ├── TrafficControl.vue
        │   │   └── VisitorTrajectory.vue
        │   ├── enforcement/                    # 执法监管模块
        │   │   ├── IllegalBehavior.vue
        │   │   ├── EnforcementDispatch.vue
        │   │   └── SurveillancePoint.vue
        │   ├── research/                       # 科研支撑模块
        │   │   ├── ResearchProject.vue
        │   │   ├── DataCollection.vue
        │   │   └── ResearchAchievement.vue
        │   └── system/                         # 系统管理模块
        │       ├── UserManagement.vue
        │       └── AreaManagement.vue
        │
        ├── components/                         # 公共组件(待实现)
        │   ├── Header.vue                      # 页头
        │   ├── Sidebar.vue                     # 侧边栏
        │   ├── Breadcrumb.vue                  # 面包屑
        │   └── ...
        │
        ├── layouts/                            # 布局组件(待实现)
        │   └── MainLayout.vue                  # 主布局
        │
        └── assets/                             # 资源文件(待添加)
            ├── styles/
            └── images/
```

## 文件功能说明

### 后端核心文件

#### 1. `backend/national_park/settings.py`
**功能:** Django项目核心配置
**关键配置:**
- 数据库连接(MySQL)
- CORS跨域设置
- JWT认证配置
- REST Framework配置
- 日志配置
- 会话管理

**重要设置:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'national_park_system',
        # 使用环境变量配置
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

#### 2. `backend/api/models.py`
**功能:** 定义21个Django模型,对应数据库表
**特点:**
- `managed=False` - 不让Django管理表结构
- 保留数据库约束和索引定义
- 使用CharField作为主键(与数据库一致)
- 完整的中文verbose_name

**模型列表:**
```python
FunctionalArea        # 功能分区
SystemUser           # 系统用户
UserSession          # 用户会话
Species              # 物种
Habitat              # 栖息地
MonitoringDevice     # 监测设备
MonitoringRecord     # 监测记录
HabitatSpecies       # 栖息地物种关联
MonitoringIndicator  # 监测指标
EnvironmentalData    # 环境数据
Visitor              # 游客
Reservation          # 预约记录
VisitorTrajectory    # 游客轨迹
TrafficControl       # 流量控制
LawEnforcer          # 执法人员
SurveillancePoint    # 监控点
IllegalBehavior      # 非法行为
EnforcementDispatch  # 执法调度
ResearchProject      # 科研项目
ResearchDataCollection  # 数据采集
ResearchAchievement  # 科研成果
```

#### 3. `backend/api/serializers.py`
**功能:** DRF序列化器,按业务线组织
**结构:**
- 基础序列化器(FunctionalArea, SystemUser等)
- 生物多样性序列化器(Species, Habitat, MonitoringRecord等)
- 环境监测序列化器(EnvironmentalData, Indicator等)
- 游客管理序列化器(Visitor, Reservation, TrafficControl等)
- 执法监管序列化器(IllegalBehavior, Dispatch等)
- 科研支撑序列化器(Project, Achievement等)
- 统计序列化器(BiodiversityStats, VisitorStats等)

**特点:**
- 分离读写序列化器(List/Detail/Create)
- 嵌套序列化器显示关联信息
- 自定义验证逻辑
- 统计数据序列化器

### 前端核心文件

#### 4. `frontend/src/router/index.js`
**功能:** Vue Router配置 + 路由守卫
**特点:**
- 懒加载路由组件
- 基于角色的路由权限控制
- 自动登录检查
- 未授权自动跳转

**路由结构:**
```javascript
/login                              # 登录页
/                                   # 主布局
  /dashboard                        # 仪表盘
  /biodiversity/*                   # 生物多样性模块
  /environment/*                    # 环境监测模块
  /visitor/*                        # 游客管理模块
  /enforcement/*                    # 执法监管模块
  /research/*                       # 科研支撑模块
  /system/*                         # 系统管理模块
```

#### 5. `frontend/src/store/auth.js`
**功能:** Pinia认证状态管理
**状态:**
- `token` - JWT访问令牌
- `user` - 当前用户信息
- `isAuthenticated` - 登录状态

**方法:**
- `login()` - 用户登录
- `logout()` - 用户登出
- `fetchUserInfo()` - 获取用户信息
- `checkAuth()` - 检查登录状态

#### 6. `frontend/src/utils/request.js`
**功能:** Axios封装 + 请求/响应拦截器
**特点:**
- 自动添加JWT Token
- 统一错误处理
- 401自动跳转登录
- Element Plus消息提示

#### 7. `frontend/src/api/*.js`
**功能:** API服务层,按业务线封装
**文件:**
- `auth.js` - 认证相关(登录、登出、获取用户信息)
- `biodiversity.js` - 生物多样性(物种、栖息地、监测记录)
- `environment.js` - 环境监测(环境数据、指标、设备)
- `visitor.js` - 游客管理(游客、预约、流量、轨迹)
- `enforcement.js` - 执法监管(违法行为、调度、监控点)
- `research.js` - 科研支撑(项目、数据采集、成果)

**API命名规范:**
```javascript
get{Entity}List()       # 获取列表
get{Entity}Detail()     # 获取详情
create{Entity}()        # 创建
update{Entity}()        # 更新
delete{Entity}()        # 删除
{action}{Entity}()      # 自定义操作
```

## 数据流向

### 1. 用户请求流程
```
用户操作
  ↓
Vue组件
  ↓
调用API服务 (api/*.js)
  ↓
Axios请求 (utils/request.js)
  ↓
Django REST API (api/views.py)
  ↓
DRF序列化器验证 (api/serializers.py)
  ↓
Django ORM查询 (api/models.py)
  ↓
MySQL数据库
```

### 2. 认证流程
```
用户输入账号密码
  ↓
调用login API
  ↓
Django验证用户
  ↓
返回JWT Token
  ↓
存储到localStorage
  ↓
Pinia更新认证状态
  ↓
后续请求自动携带Token
```

### 3. 权限控制流程
```
前端路由守卫检查角色
  ↓
后端DRF权限类验证
  ↓
双重验证通过
  ↓
返回数据
```

## 开发规范

### 1. 命名规范
- **Vue组件:** PascalCase (如 `SpeciesManagement.vue`)
- **API文件:** camelCase (如 `biodiversity.js`)
- **API函数:** camelCase (如 `getSpeciesList()`)
- **Django模型:** PascalCase (如 `Species`)
- **序列化器:** PascalCase + Serializer (如 `SpeciesSerializer`)

### 2. 代码组织
- **按业务线分模块** - 5条业务线对应5个目录
- **分离关注点** - API层、状态层、视图层分离
- **复用组件** - 公共组件放components目录

### 3. 注释规范
- **文件头注释** - 说明文件功能
- **函数注释** - JSDoc/Docstring格式
- **关键逻辑注释** - 解释复杂业务逻辑

## 待实现功能清单

### 后端
- [ ] API Views (ViewSet + APIView)
- [ ] URL路由配置
- [ ] 权限类实现
- [ ] 统计接口实现
- [ ] 文件上传处理
- [ ] 单元测试

### 前端
- [ ] 登录页面
- [ ] 仪表盘
- [ ] 20+业务页面
- [ ] 公共组件(Header, Sidebar等)
- [ ] 主布局组件
- [ ] ECharts图表
- [ ] 表单验证
- [ ] 文件上传组件

## 部署架构

```
                        [Nginx]
                          |
                    负载均衡/反向代理
                          |
            +-------------+-------------+
            |                           |
      [Frontend]                   [Backend]
    (Vue静态文件)              (Django + Gunicorn)
                                      |
                                  [MySQL]
```

## 性能优化建议

1. **前端优化**
   - 路由懒加载
   - 组件按需加载
   - 图片懒加载
   - Vite构建优化

2. **后端优化**
   - 数据库查询优化(使用现有索引)
   - Redis缓存(可选)
   - 分页查询
   - select_related/prefetch_related

3. **数据库优化**
   - 使用已创建的44个索引
   - 使用视图简化查询
   - 使用存储过程处理复杂逻辑

---

**最后更新:** 2025-12-30
