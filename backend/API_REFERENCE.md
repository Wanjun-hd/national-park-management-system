# API 快速参考 Quick Reference

## 基础信息

- **Base URL**: `http://127.0.0.1:8000/api/`
- **认证方式**: JWT Bearer Token
- **内容类型**: `application/json`

## 认证 Authentication

### 登录
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}

Response 200:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "user_id": "U001",
        "username": "admin",
        "real_name": "系统管理员",
        "role_type": "系统管理员"
    }
}
```

### 刷新 Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your-refresh-token"
}
```

### 创建测试用户
```http
POST /api/auth/create-test-user/
```

## 生物多样性 Biodiversity

### 物种管理

#### 获取物种列表
```http
GET /api/biodiversity/species/
Authorization: Bearer {access_token}

# 筛选
GET /api/biodiversity/species/?protection_level=国家一级保护
GET /api/biodiversity/species/?kingdom=动物界
GET /api/biodiversity/species/?phylum=脊索动物门

# 搜索
GET /api/biodiversity/species/?search=大熊猫

# 排序
GET /api/biodiversity/species/?ordering=chinese_name
GET /api/biodiversity/species/?ordering=-species_id

# 分页
GET /api/biodiversity/species/?page=2&page_size=20
```

#### 获取物种详情
```http
GET /api/biodiversity/species/{species_id}/
Authorization: Bearer {access_token}
```

#### 创建物种
```http
POST /api/biodiversity/species/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "species_id": "S001",
    "chinese_name": "大熊猫",
    "latin_name": "Ailuropoda melanoleuca",
    "kingdom": "动物界",
    "phylum": "脊索动物门",
    "class_name": "哺乳纲",
    "order": "食肉目",
    "family": "熊科",
    "protection_level": "国家一级保护"
}
```

#### 更新物种
```http
PUT /api/biodiversity/species/{species_id}/
PATCH /api/biodiversity/species/{species_id}/
Authorization: Bearer {access_token}
```

#### 删除物种
```http
DELETE /api/biodiversity/species/{species_id}/
Authorization: Bearer {access_token}
```

#### 获取受保护物种列表
```http
GET /api/biodiversity/species/protected/
Authorization: Bearer {access_token}
```

#### 获取物种统计
```http
GET /api/biodiversity/species/statistics/
Authorization: Bearer {access_token}

Response 200:
{
    "total": 150,
    "by_protection_level": {
        "国家一级保护": 20,
        "国家二级保护": 35,
        "无": 95
    },
    "by_kingdom": {
        "动物界": 80,
        "植物界": 70
    }
}
```

### 栖息地管理

```http
GET /api/biodiversity/habitats/
POST /api/biodiversity/habitats/
GET /api/biodiversity/habitats/{id}/
PUT /api/biodiversity/habitats/{id}/
DELETE /api/biodiversity/habitats/{id}/

# 筛选
GET /api/biodiversity/habitats/?ecology_type=森林

# 搜索
GET /api/biodiversity/habitats/?search=核心区
```

### 监测设备管理

```http
GET /api/biodiversity/devices/
POST /api/biodiversity/devices/
GET /api/biodiversity/devices/{id}/
PUT /api/biodiversity/devices/{id}/
DELETE /api/biodiversity/devices/{id}/

# 筛选
GET /api/biodiversity/devices/?operation_status=正常
GET /api/biodiversity/devices/?device_type=红外相机
```

#### 更新设备状态
```http
POST /api/biodiversity/devices/{device_id}/update_status/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "operation_status": "故障"
}
```

### 监测记录管理

```http
GET /api/biodiversity/monitoring-records/
POST /api/biodiversity/monitoring-records/
GET /api/biodiversity/monitoring-records/{id}/
PUT /api/biodiversity/monitoring-records/{id}/
DELETE /api/biodiversity/monitoring-records/{id}/

# 筛选
GET /api/biodiversity/monitoring-records/?species=S001
GET /api/biodiversity/monitoring-records/?monitoring_method=红外相机
GET /api/biodiversity/monitoring-records/?data_status=有效

# 排序
GET /api/biodiversity/monitoring-records/?ordering=-monitoring_time
```

## 环境监测 Environment

### 监测指标管理

```http
GET /api/environment/indicators/
POST /api/environment/indicators/
GET /api/environment/indicators/{id}/
PUT /api/environment/indicators/{id}/
DELETE /api/environment/indicators/{id}/

# 搜索
GET /api/environment/indicators/?search=温度
```

### 环境数据管理

```http
GET /api/environment/data/
POST /api/environment/data/
GET /api/environment/data/{id}/
PUT /api/environment/data/{id}/
DELETE /api/environment/data/{id}/

# 筛选
GET /api/environment/data/?indicator=IND001
GET /api/environment/data/?area=A001
GET /api/environment/data/?data_quality=优秀

# 排序
GET /api/environment/data/?ordering=-collection_time
```

#### 环境数据统计
```http
GET /api/environment/data/stats/?indicator_id=IND001
Authorization: Bearer {access_token}

Response 200:
{
    "indicator_name": "温度",
    "avg_value": 18.5,
    "max_value": 32.0,
    "min_value": -5.0,
    "count": 1250
}
```

## 游客管理 Visitor

### 游客管理

```http
GET /api/visitor/visitors/
POST /api/visitor/visitors/
GET /api/visitor/visitors/{id}/
PUT /api/visitor/visitors/{id}/
DELETE /api/visitor/visitors/{id}/

# 搜索
GET /api/visitor/visitors/?search=张三
GET /api/visitor/visitors/?search=13812345678

# 排序
GET /api/visitor/visitors/?ordering=-entry_time
```

### 预约管理

```http
GET /api/visitor/reservations/
POST /api/visitor/reservations/
GET /api/visitor/reservations/{id}/
PUT /api/visitor/reservations/{id}/
DELETE /api/visitor/reservations/{id}/

# 筛选
GET /api/visitor/reservations/?reservation_status=已确认
GET /api/visitor/reservations/?payment_status=已支付

# 排序
GET /api/visitor/reservations/?ordering=-reservation_date
```

#### 取消预约
```http
POST /api/visitor/reservations/{reservation_id}/cancel/
Authorization: Bearer {access_token}

Response 200:
{
    "detail": "预约已取消"
}
```

### 流量控制

```http
GET /api/visitor/traffic-controls/
POST /api/visitor/traffic-controls/
GET /api/visitor/traffic-controls/{id}/
PUT /api/visitor/traffic-controls/{id}/
DELETE /api/visitor/traffic-controls/{id}/
```

#### 流量统计
```http
GET /api/visitor/traffic-controls/stats/
Authorization: Bearer {access_token}

Response 200:
[
    {
        "area_name": "核心区",
        "utilization_rate": 75.5,
        "current_visitor_count": 151,
        "daily_capacity": 200,
        "current_status": "正常开放"
    }
]
```

## 执法监管 Enforcement

### 违法行为管理

```http
GET /api/enforcement/illegal-behaviors/
POST /api/enforcement/illegal-behaviors/
GET /api/enforcement/illegal-behaviors/{id}/
PUT /api/enforcement/illegal-behaviors/{id}/
DELETE /api/enforcement/illegal-behaviors/{id}/

# 筛选
GET /api/enforcement/illegal-behaviors/?handling_status=未处理
GET /api/enforcement/illegal-behaviors/?area=A001

# 排序
GET /api/enforcement/illegal-behaviors/?ordering=-occurrence_time
```

#### 处理违法行为
```http
POST /api/enforcement/illegal-behaviors/{behavior_id}/handle/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "handling_result": "罚款500元",
    "penalty_basis": "《国家公园管理条例》第XX条",
    "enforcer_id": "U003"
}

Response 200:
{
    "detail": "处理完成"
}
```

### 执法调度

```http
GET /api/enforcement/dispatches/
POST /api/enforcement/dispatches/
GET /api/enforcement/dispatches/{id}/
PUT /api/enforcement/dispatches/{id}/
DELETE /api/enforcement/dispatches/{id}/

# 筛选
GET /api/enforcement/dispatches/?dispatch_status=已处理
GET /api/enforcement/dispatches/?enforcer=U003
```

## 科研支撑 Research

### 科研项目管理

```http
GET /api/research/projects/
POST /api/research/projects/
GET /api/research/projects/{id}/
PUT /api/research/projects/{id}/
DELETE /api/research/projects/{id}/

# 筛选
GET /api/research/projects/?project_status=在研
GET /api/research/projects/?research_field=生态学

# 搜索
GET /api/research/projects/?search=大熊猫栖息地
```

### 科研数据采集

```http
GET /api/research/data-collections/
POST /api/research/data-collections/
GET /api/research/data-collections/{id}/
PUT /api/research/data-collections/{id}/
DELETE /api/research/data-collections/{id}/

# 筛选
GET /api/research/data-collections/?project=P001
GET /api/research/data-collections/?data_source=实地考察
```

### 科研成果管理

```http
GET /api/research/achievements/
POST /api/research/achievements/
GET /api/research/achievements/{id}/
PUT /api/research/achievements/{id}/
DELETE /api/research/achievements/{id}/

# 筛选
GET /api/research/achievements/?achievement_type=论文
GET /api/research/achievements/?share_permission=公开
```

## 统计分析 Statistics

### 仪表盘统计
```http
GET /api/dashboard/stats/
Authorization: Bearer {access_token}

Response 200:
{
    "biodiversity": {
        "total_species": 150,
        "protected_species": 55,
        "monitoring_records": 3200,
        "active_devices": 45
    },
    "environment": {
        "total_indicators": 8,
        "total_data_points": 15600,
        "devices": 32
    },
    "visitor": {
        "total_visitors": 12500,
        "current_in_park": 235,
        "reservations_today": 89
    },
    "enforcement": {
        "total_illegal_behaviors": 45,
        "unhandled": 3,
        "in_progress": 8
    },
    "research": {
        "total_projects": 12,
        "ongoing_projects": 7,
        "total_achievements": 28
    }
}
```

### 测试 API
```http
GET /api/test/

Response 200:
{
    "status": "success",
    "message": "后端API正常运行",
    "version": "1.0.0",
    "timestamp": "2025-12-30T10:30:00"
}
```

## 响应状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容） |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 通用查询参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `page` | 页码 | `?page=2` |
| `page_size` | 每页数量 | `?page_size=50` |
| `search` | 搜索关键词 | `?search=大熊猫` |
| `ordering` | 排序字段（-表示降序） | `?ordering=-created_at` |

## 认证头部

所有需要认证的请求都需要添加以下头部：

```http
Authorization: Bearer {access_token}
```

## 错误响应格式

```json
{
    "success": false,
    "error": {
        "code": 400,
        "message": "数据验证失败",
        "details": {
            "field": ["错误详情"]
        }
    }
}
```

## 分页响应格式

```json
{
    "count": 150,
    "next": "http://127.0.0.1:8000/api/species/?page=2",
    "previous": null,
    "results": [...]
}
```

## 常用示例

### 创建监测记录
```http
POST /api/biodiversity/monitoring-records/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "species": "S001",
    "device": "D001",
    "monitoring_time": "2025-12-30T10:30:00",
    "monitoring_method": "红外相机",
    "quantity": 2,
    "behavior_description": "在栖息地活动",
    "data_status": "有效",
    "recorder": "U002"
}
```

### 创建预约
```http
POST /api/visitor/reservations/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "visitor": "V001",
    "reservation_date": "2025-12-31",
    "visitor_count": 4,
    "total_amount": 400.00,
    "payment_status": "已支付",
    "reservation_status": "已确认"
}
```

### 记录环境数据
```http
POST /api/environment/data/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "indicator": "IND001",
    "device": "D010",
    "area": "A001",
    "collection_time": "2025-12-30T10:00:00",
    "monitoring_value": 18.5,
    "data_quality": "优秀"
}
```

## API 文档

访问交互式 API 文档：

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/

## 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 系统管理员 |
| monitor | monitor123 | 生态监测员 |

---

**更多详情请查看**: [完整 API 文档](http://127.0.0.1:8000/api/docs/)
