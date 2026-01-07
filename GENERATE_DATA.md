# 生成测试数据

系统已经更新为简洁的设计风格，现在需要生成测试数据来显示仪表盘的统计信息。

## 方法1：使用MySQL命令行

1. 打开MySQL命令行或MySQL Workbench

2. 执行以下命令：
```bash
mysql -u root -p national_park_system < backend\generate_test_data.sql
```

或者在MySQL Workbench中：
- File -> Open SQL Script
- 选择 `backend\generate_test_data.sql`
- 点击执行（闪电图标）

## 方法2：手动复制SQL

1. 打开 `backend\generate_test_data.sql` 文件

2. 复制所有SQL语句

3. 在MySQL客户端中执行

## 数据说明

生成的测试数据包括：
- 10条物种数据（包括大熊猫、金丝猴、朱鹮等）
- 4个栖息地
- 5个监测设备
- 5条监测记录
- 5个环境指标
- 5条环境数据
- 5个游客记录
- 5条预约记录
- 4条违法行为记录
- 4个科研项目

## 执行后效果

数据生成后，刷新前端页面，仪表盘将显示：
- 物种总数：10
- 受保护物种：10
- 监测设备：5
- 监测记录：5条
- 游客数量：5
- 预约记录：5条
- 违法行为：4条
- 科研项目：4个

## 注意事项

- 如果数据已存在，`INSERT IGNORE` 将跳过重复记录
- 确保数据库中已有必需的关联数据（如 area_id: A001, A002, A003, user_id: U002等）
- 如果关联数据不存在，可能需要先创建这些基础数据
