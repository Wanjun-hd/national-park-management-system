-- 生成测试数据SQL脚本

-- 1. 插入物种数据
INSERT IGNORE INTO species (species_id, chinese_name, latin_name, kingdom, phylum, class, order_name, family, genus, species_name, protection_level) VALUES
('S001', '大熊猫', 'Ailuropoda melanoleuca', '动物界', '脊索动物门', '哺乳纲', '食肉目', '熊科', 'Ailuropoda', 'melanoleuca', '国家一级'),
('S002', '金丝猴', 'Rhinopithecus roxellana', '动物界', '脊索动物门', '哺乳纲', '灵长目', '猴科', 'Rhinopithecus', 'roxellana', '国家一级'),
('S003', '朱鹮', 'Nipponia nippon', '动物界', '脊索动物门', '鸟纲', '鹳形目', '朱鹮科', 'Nipponia', 'nippon', '国家一级'),
('S004', '东北虎', 'Panthera tigris altaica', '动物界', '脊索动物门', '哺乳纲', '食肉目', '猫科', 'Panthera', 'tigris', '国家一级'),
('S005', '雪豹', 'Panthera uncia', '动物界', '脊索动物门', '哺乳纲', '食肉目', '猫科', 'Panthera', 'uncia', '国家一级'),
('S006', '藏羚羊', 'Pantholops hodgsonii', '动物界', '脊索动物门', '哺乳纲', '偶蹄目', '牛科', 'Pantholops', 'hodgsonii', '国家一级'),
('S007', '野牦牛', 'Bos mutus', '动物界', '脊索动物门', '哺乳纲', '偶蹄目', '牛科', 'Bos', 'mutus', '国家一级'),
('S008', '黑颈鹤', 'Grus nigricollis', '动物界', '脊索动物门', '鸟纲', '鹤形目', '鹤科', 'Grus', 'nigricollis', '国家一级'),
('S009', '红豆杉', 'Taxus chinensis', '植物界', '松柏门', '松柏纲', '松柏目', '红豆杉科', 'Taxus', 'chinensis', '国家一级'),
('S010', '珙桐', 'Davidia involucrata', '植物界', '被子植物门', '双子叶植物纲', '蔷薇目', '珙桐科', 'Davidia', 'involucrata', '国家一级');

-- 2. 插入栖息地数据
INSERT IGNORE INTO habitat (habitat_id, area_name, ecology_type, area_size, suitability_score) VALUES
('H001', '核心保护区1号', '森林', 1500.00, 9.5),
('H002', '缓冲区2号', '森林', 800.00, 8.7),
('H003', '实验区3号', '草原', 1200.00, 8.2),
('H004', '湿地保护区', '湿地', 600.00, 9.1);

-- 3. 插入监测设备数据
INSERT IGNORE INTO monitoring_device (device_id, location, device_name, device_type, operation_status, installation_date) VALUES
('D001', 'H001', '红外相机01', '红外相机', '正常', '2024-01-01'),
('D002', 'H001', '红外相机02', '红外相机', '正常', '2024-01-01'),
('D003', 'H002', '红外相机03', '红外相机', '正常', '2024-01-01'),
('D004', 'H003', 'GPS追踪器01', 'GPS追踪器', '正常', '2024-02-01'),
('D005', 'H004', '无人机01', '无人机', '正常', '2024-02-15');

-- 4. 插入监测记录数据
INSERT IGNORE INTO monitoring_record (record_id, species_id, device_id, monitoring_time, monitoring_method, quantity, behavior_description, data_status, recorder_id) VALUES
('MR001', 'S001', 'D001', '2024-12-15 10:30:00', '红外相机', 2, '正常活动', '有效', 'U002'),
('MR002', 'S001', 'D002', '2024-12-16 14:20:00', '红外相机', 1, '觅食中', '有效', 'U002'),
('MR003', 'S002', 'D001', '2024-12-17 09:15:00', '红外相机', 3, '群体活动', '有效', 'U002'),
('MR004', 'S003', 'D003', '2024-12-18 16:45:00', '红外相机', 4, '飞行', '有效', 'U002'),
('MR005', 'S005', 'D002', '2024-12-20 08:00:00', '红外相机', 1, '巡视领地', '有效', 'U002');

-- 5. 插入环境指标数据
INSERT IGNORE INTO environment_indicator (indicator_id, indicator_name, unit, min_normal_value, max_normal_value) VALUES
('IND001', '温度', '摄氏度', -10.00, 40.00),
('IND002', '湿度', '百分比', 0.00, 100.00),
('IND003', '空气质量', 'AQI', 0.00, 500.00),
('IND004', '土壤pH值', 'pH', 4.00, 9.00),
('IND005', '降水量', '毫米', 0.00, 500.00);

-- 6. 插入环境数据
INSERT IGNORE INTO environment_data (data_id, indicator_id, device_id, area_id, collection_time, monitoring_value, data_quality) VALUES
('ED0001', 'IND001', 'D001', 'A001', '2024-12-25 08:00:00', 18.50, '优秀'),
('ED0002', 'IND002', 'D001', 'A001', '2024-12-25 08:00:00', 65.30, '优秀'),
('ED0003', 'IND003', 'D001', 'A001', '2024-12-25 08:00:00', 45.00, '优秀'),
('ED0004', 'IND001', 'D002', 'A001', '2024-12-25 09:00:00', 19.20, '优秀'),
('ED0005', 'IND002', 'D002', 'A001', '2024-12-25 09:00:00', 63.80, '优秀');

-- 7. 插入游客数据
INSERT IGNORE INTO visitor (visitor_id, name, id_card, phone, entry_time) VALUES
('V001', '张三', '110101199001011234', '13800138001', '2024-12-28 09:30:00'),
('V002', '李四', '110101199002021234', '13800138002', '2024-12-28 10:00:00'),
('V003', '王五', '110101199003031234', '13800138003', '2024-12-28 10:30:00'),
('V004', '赵六', '110101199004041234', '13800138004', '2024-12-28 11:00:00'),
('V005', '钱七', '110101199005051234', '13800138005', '2024-12-28 11:30:00');

-- 8. 插入预约数据
INSERT IGNORE INTO reservation (reservation_id, visitor_id, reservation_date, visitor_count, contact_phone, total_amount, payment_status, reservation_status) VALUES
('R0001', 'V001', '2025-01-05', 2, '13800138001', 200.00, '已支付', '已确认'),
('R0002', 'V002', '2025-01-06', 3, '13800138002', 300.00, '已支付', '已确认'),
('R0003', 'V003', '2025-01-07', 1, '13800138003', 100.00, '未支付', '待确认'),
('R0004', 'V004', '2025-01-08', 4, '13800138004', 400.00, '已支付', '已确认'),
('R0005', 'V005', '2025-01-09', 2, '13800138005', 200.00, '已支付', '已确认');

-- 9. 插入违法行为数据
INSERT IGNORE INTO illegal_behavior (behavior_id, occurrence_time, area_id, behavior_type, severity_level, description, handling_status, reporter_id) VALUES
('IB001', '2024-12-20 14:30:00', 'A001', '非法狩猎', '严重', '发现非法捕猎行为', '已处理', 'U002'),
('IB002', '2024-12-22 16:00:00', 'A002', '乱扔垃圾', '轻微', '游客随意丢弃垃圾', '已处理', 'U002'),
('IB003', '2024-12-24 10:15:00', 'A001', '破坏植被', '一般', '采摘珍稀植物', '处理中', 'U002'),
('IB004', '2024-12-26 13:45:00', 'A003', '非法采集', '一般', '非法采集矿产资源', '未处理', 'U002');

-- 10. 插入科研项目数据
INSERT IGNORE INTO research_project (project_id, project_name, research_field, project_status, start_date, leader_id) VALUES
('P001', '大熊猫栖息地生态研究', '生态学', '在研', '2024-01-01', 'U002'),
('P002', '生物多样性调查与监测', '生物学', '在研', '2024-02-01', 'U002'),
('P003', '气候变化对物种影响研究', '环境科学', '在研', '2024-03-01', 'U002'),
('P004', '野生动物保护技术研发', '保护生物学', '已结题', '2023-06-01', 'U002');
