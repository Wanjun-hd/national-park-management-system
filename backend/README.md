# 国家公园管理系统 - 后端 API

基于 Django + Django REST Framework 的国家公园综合管理系统后端服务。

## 技术栈

- **框架**: Django 4.2.7
- **REST API**: Django REST Framework 3.14.0
- **数据库**: MySQL 8.0
- **认证**: JWT (djangorestframework-simplejwt)
- **API文档**: drf-spectacular (Swagger/OpenAPI)
- **其他**: CORS支持、数据过滤、分页

## 功能模块

### 1. 认证模块
- JWT Token 认证
- 用户登录/登出
- 账号锁定机制（5次失败尝试）
- SHA-256 密码加密

### 2. 生物多样性监测
- 物种信息管理（CRUD）
- 栖息地管理
- 监测设备管理
- 监测记录管理
- 受保护物种列表
- 物种统计分析

### 3. 环境监测
- 监测指标管理
- 环境数据采集
- 数据质量控制
- 环境数据统计

### 4. 游客管理
- 游客信息管理
- 预约系统
- 流量控制
- 预约取消功能
- 流量统计

### 5. 执法监管
- 违法行为记录
- 执法调度
- 案件处理流程
- 执法统计

### 6. 科研支撑
- 科研项目管理
- 数据采集管理
- 科研成果管理
- 数据访问权限控制

### 7. 统计分析
- 综合仪表盘数据
- 各模块统计信息
- 数据可视化支持

## 项目结构

```
backend/
├── api/                        # API应用
│   ├── migrations/            # 数据库迁移文件
│   ├── __init__.py
│   ├── admin.py              # Django管理后台
│   ├── apps.py               # 应用配置
│   ├── models.py             # 数据模型（21个表）
│   ├── serializers.py        # DRF序列化器
│   ├── views.py              # API视图
│   ├── urls.py               # API路由
│   ├── permissions.py        # 自定义权限类
│   ├── validators.py         # 数据验证器
│   ├── exceptions.py         # 自定义异常处理
│   └── utils.py              # 工具函数
├── national_park/            # 项目配置
│   ├── __init__.py
│   ├── settings.py           # 项目设置
│   ├── urls.py               # 主路由
│   ├── wsgi.py              # WSGI配置
│   └── asgi.py              # ASGI配置
├── logs/                     # 日志目录
├── media/                    # 媒体文件
├── staticfiles/              # 静态文件
├── .env                      # 环境变量
├── .env.example             # 环境变量示例
├── manage.py                # Django管理脚本
└── requirements.txt         # Python依赖

```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

复制 `.env.example` 为 `.env` 并配置数据库连接：

```env
# 数据库配置
DB_NAME=national_park_system
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Django配置
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT配置
JWT_ACCESS_TOKEN_LIFETIME=30      # 分钟
JWT_REFRESH_TOKEN_LIFETIME=1440   # 分钟（24小时）
```

### 3. 数据库初始化

确保MySQL数据库已经存在并运行了DDL脚本：

```bash
# 检查数据库连接
python manage.py check

# 创建Django表（可选，因为使用了managed=False）
python manage.py migrate
```

### 4. 创建测试用户

```bash
# 运行开发服务器
python manage.py runserver

# 访问创建测试用户接口
# POST http://localhost:8000/api/auth/create-test-user/
```

或者直接在浏览器访问登录页面，点击"创建测试账号"按钮。

**测试账号**:
- 管理员: `admin` / `admin123`
- 生态监测员: `monitor` / `monitor123`

### 5. 运行服务器

```bash
python manage.py runserver
```

服务器将在 `http://127.0.0.1:8000/` 启动。

## API 文档

### 访问 API 文档

启动服务器后，访问以下地址查看完整API文档：

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

### API 端点概览

#### 认证相关
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/create-test-user/` - 创建测试用户
- `POST /api/token/` - 获取JWT Token
- `POST /api/token/refresh/` - 刷新Token
- `POST /api/token/verify/` - 验证Token

#### 生物多样性
- `GET/POST /api/biodiversity/species/` - 物种列表/创建
- `GET/PUT/DELETE /api/biodiversity/species/{id}/` - 物种详情/更新/删除
- `GET /api/biodiversity/species/protected/` - 受保护物种列表
- `GET /api/biodiversity/species/statistics/` - 物种统计
- `GET/POST /api/biodiversity/habitats/` - 栖息地管理
- `GET/POST /api/biodiversity/devices/` - 监测设备管理
- `GET/POST /api/biodiversity/monitoring-records/` - 监测记录管理

#### 环境监测
- `GET/POST /api/environment/indicators/` - 监测指标管理
- `GET/POST /api/environment/data/` - 环境数据管理
- `GET /api/environment/data/stats/` - 环境数据统计

#### 游客管理
- `GET/POST /api/visitor/visitors/` - 游客管理
- `GET/POST /api/visitor/reservations/` - 预约管理
- `POST /api/visitor/reservations/{id}/cancel/` - 取消预约
- `GET/POST /api/visitor/traffic-controls/` - 流量控制
- `GET /api/visitor/traffic-controls/stats/` - 流量统计

#### 执法监管
- `GET/POST /api/enforcement/illegal-behaviors/` - 违法行为管理
- `POST /api/enforcement/illegal-behaviors/{id}/handle/` - 处理违法行为
- `GET/POST /api/enforcement/dispatches/` - 执法调度管理

#### 科研支撑
- `GET/POST /api/research/projects/` - 科研项目管理
- `GET/POST /api/research/data-collections/` - 数据采集管理
- `GET/POST /api/research/achievements/` - 科研成果管理

#### 统计分析
- `GET /api/dashboard/stats/` - 仪表盘统计数据
- `GET /api/test/` - API测试接口

## 核心特性

### 1. 权限控制系统

基于角色的访问控制（RBAC），支持8种用户角色：

- 系统管理员
- 生态监测员
- 环境监测员
- 游客管理员
- 执法人员
- 科研人员
- 保护区管理员
- 数据分析员

自定义权限类（`api/permissions.py`）：
```python
from api.permissions import IsSystemAdmin, IsEcologyMonitor

class SpeciesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEcologyMonitor]
```

### 2. 数据验证系统

完整的数据验证器（`api/validators.py`）：
- 手机号码验证
- 身份证号验证
- 邮箱验证
- 地理坐标验证
- 日期范围验证
- 业务数据验证

使用示例：
```python
from api.validators import validate_phone_number

validate_phone_number('13812345678')  # 验证通过
```

### 3. 异常处理系统

统一的异常处理机制（`api/exceptions.py`）：
- 自定义业务异常
- 标准化错误响应格式
- 友好的错误提示

异常响应格式：
```json
{
    "success": false,
    "error": {
        "code": 400,
        "message": "错误描述",
        "details": "详细信息"
    }
}
```

### 4. 工具函数库

丰富的工具函数（`api/utils.py`）：
- ID生成器
- 密码加密
- 日期处理
- 距离计算
- 数据导出
- 统计分析

### 5. API 文档自动生成

使用 drf-spectacular 自动生成 OpenAPI 3.0 文档：
- 交互式 Swagger UI
- 美观的 ReDoc 文档
- 支持在线测试
- 自动类型推断

### 6. 数据过滤与搜索

支持多种数据过滤方式：
- 精确匹配过滤
- 模糊搜索
- 日期范围过滤
- 排序

示例：
```
GET /api/biodiversity/species/?protection_level=国家一级保护&search=大熊猫
```

### 7. 分页支持

自动分页，默认每页20条记录：
```json
{
    "count": 100,
    "next": "http://api/species/?page=2",
    "previous": null,
    "results": [...]
}
```

## 数据模型

系统包含21个核心数据表：

### 用户与权限
- SystemUser - 系统用户
- Role - 角色
- Permission - 权限

### 生物多样性
- Species - 物种
- Habitat - 栖息地
- MonitoringDevice - 监测设备
- MonitoringRecord - 监测记录

### 环境监测
- MonitoringIndicator - 监测指标
- EnvironmentalData - 环境数据

### 游客管理
- Visitor - 游客
- Reservation - 预约
- TrafficControl - 流量控制

### 执法监管
- IllegalBehavior - 违法行为
- EnforcementDispatch - 执法调度

### 科研支撑
- ResearchProject - 科研项目
- ResearchDataCollection - 数据采集
- ResearchAchievement - 科研成果

### 基础数据
- ProtectionArea - 保护区域
- Organization - 组织机构
- SystemLog - 系统日志
- DataChangeLog - 数据变更日志

所有模型都设置了 `managed=False`，使用现有数据库结构。

## 开发指南

### 添加新的API端点

1. 在 `models.py` 中定义或引用模型
2. 在 `serializers.py` 中创建序列化器
3. 在 `views.py` 中创建 ViewSet 或视图函数
4. 在 `urls.py` 中注册路由
5. 添加权限控制和数据验证

示例：
```python
# serializers.py
class NewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewModel
        fields = '__all__'

# views.py
@extend_schema_view(
    list=extend_schema(tags=['新模块'], summary='列表'),
)
class NewModelViewSet(viewsets.ModelViewSet):
    queryset = NewModel.objects.all()
    serializer_class = NewModelSerializer
    permission_classes = [IsAuthenticated]

# urls.py
router.register(r'new-models', views.NewModelViewSet, basename='new-model')
```

### 自定义验证

在 `validators.py` 中添加验证器：
```python
def validate_custom_field(value):
    if not meets_condition(value):
        raise ValidationError('验证失败原因')
```

在序列化器中使用：
```python
from api.validators import validate_custom_field

class MySerializer(serializers.ModelSerializer):
    custom_field = serializers.CharField(validators=[validate_custom_field])
```

### 自定义权限

在 `permissions.py` 中添加权限类：
```python
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return check_condition(request.user)
```

在视图中使用：
```python
from api.permissions import CustomPermission

class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomPermission]
```

## 安全特性

1. **JWT认证**: 使用 JWT Token 进行身份验证
2. **密码加密**: SHA-256 哈希加密
3. **账号锁定**: 5次登录失败自动锁定
4. **CORS配置**: 限制跨域访问
5. **SQL注入防护**: Django ORM 自动处理
6. **XSS防护**: DRF 自动转义
7. **CSRF保护**: Django 内置保护
8. **敏感数据遮蔽**: 工具函数支持数据脱敏

## 性能优化

1. **数据库查询优化**: 使用 `select_related` 和 `prefetch_related`
2. **分页**: 自动分页减少数据传输
3. **缓存**: 可配置 Redis 缓存
4. **索引**: 数据库表已建立适当索引
5. **日志**: 异步日志处理

## 日志系统

日志文件位置: `logs/django.log`

日志级别：
- DEBUG: 开发调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误

查看日志：
```bash
tail -f logs/django.log
```

## 测试

运行测试：
```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test api

# 生成测试覆盖率报告
coverage run --source='.' manage.py test
coverage report
```

## 部署

### 生产环境配置

1. 修改 `.env` 文件：
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

2. 收集静态文件：
```bash
python manage.py collectstatic
```

3. 使用 Gunicorn 运行：
```bash
pip install gunicorn
gunicorn national_park.wsgi:application --bind 0.0.0.0:8000
```

4. 配置 Nginx 反向代理：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

## 常见问题

### 1. 数据库连接失败
- 检查 MySQL 服务是否运行
- 验证 `.env` 中的数据库配置
- 确认数据库已创建

### 2. 导入错误
```bash
ModuleNotFoundError: No module named 'xxx'
```
解决: `pip install -r requirements.txt`

### 3. 迁移错误
- 由于使用 `managed=False`，不需要运行迁移
- 如果需要创建Django内置表：`python manage.py migrate`

### 4. 端口占用
```bash
Error: That port is already in use.
```
解决: 使用其他端口 `python manage.py runserver 8001`

## 维护与更新

### 更新依赖
```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

### 数据库备份
```bash
# 备份
mysqldump -u root -p national_park_system > backup.sql

# 恢复
mysql -u root -p national_park_system < backup.sql
```

## 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题，请提交 Issue 或联系项目维护者。

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
