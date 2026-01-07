USE national_park_system;

-- ============================================
-- 视图定义脚本
-- 功能：为5条业务线创建15个实用视图
-- 创建时间：2024-12-21
-- ============================================

-- ============================================
-- 1. 生物多样性监测业务线视图（3个）
-- ============================================

-- 视图1.1：物种保护级别统计视图
DROP VIEW IF EXISTS v_species_protection_statistics;
CREATE VIEW v_species_protection_statistics AS
SELECT 
    s.protection_level AS '保护级别',
    COUNT(DISTINCT s.species_id) AS '物种总数',
    COUNT(DISTINCT mr.record_id) AS '监测记录数',
    COUNT(DISTINCT hs.habitat_id) AS '栖息地数量',
    GROUP_CONCAT(DISTINCT s.chinese_name ORDER BY s.chinese_name SEPARATOR '、') AS '物种列表',
    ROUND(COUNT(DISTINCT s.species_id) * 100.0 / 
          (SELECT COUNT(*) FROM species), 2) AS '占比(%)'
FROM species s
LEFT JOIN monitoring_record mr ON s.species_id = mr.species_id
LEFT JOIN habitat_species hs ON s.species_id = hs.species_id
GROUP BY s.protection_level
ORDER BY 
    CASE s.protection_level
        WHEN '国家一级' THEN 1
        WHEN '国家二级' THEN 2
        WHEN '无' THEN 3
    END;

-- 视图1.2：栖息地适宜性分析视图
DROP VIEW IF EXISTS v_habitat_suitability_analysis;
CREATE VIEW v_habitat_suitability_analysis AS
SELECT 
    h.habitat_id AS '栖息地编号',
    h.area_name AS '区域名称',
    h.ecology_type AS '生态类型',
    h.area_size AS '面积(公顷)',
    h.suitability_score AS '适宜性评分',
    COUNT(DISTINCT hs.species_id) AS '物种总数',
    COUNT(DISTINCT CASE WHEN hs.is_major_species = 'Y' THEN hs.species_id END) AS '主要物种数',
    COUNT(DISTINCT CASE WHEN s.protection_level IN ('国家一级', '国家二级') 
          THEN s.species_id END) AS '保护物种数',
    CASE 
        WHEN h.suitability_score >= 8 THEN '优秀'
        WHEN h.suitability_score >= 6 THEN '良好'
        WHEN h.suitability_score >= 4 THEN '一般'
        ELSE '需改善'
    END AS '适宜性等级',
    GROUP_CONCAT(DISTINCT CASE WHEN s.protection_level IN ('国家一级', '国家二级')
                 THEN s.chinese_name END ORDER BY s.protection_level SEPARATOR '、') AS '保护物种名单'
FROM habitat h
LEFT JOIN habitat_species hs ON h.habitat_id = hs.habitat_id
LEFT JOIN species s ON hs.species_id = s.species_id
GROUP BY h.habitat_id, h.area_name, h.ecology_type, h.area_size, h.suitability_score
ORDER BY h.suitability_score DESC, COUNT(DISTINCT hs.species_id) DESC;

-- 视图1.3：监测数据有效性汇总视图
DROP VIEW IF EXISTS v_monitoring_data_validity;
CREATE VIEW v_monitoring_data_validity AS
SELECT 
    DATE_FORMAT(mr.monitoring_time, '%Y-%m') AS '月份',
    mr.data_status AS '数据状态',
    COUNT(DISTINCT mr.record_id) AS '记录总数',
    COUNT(DISTINCT mr.species_id) AS '物种种类数',
    COUNT(DISTINCT mr.device_id) AS '使用设备数',
    COUNT(DISTINCT mr.recorder_id) AS '记录人员数',
    mr.monitoring_method AS '监测方式',
    ROUND(AVG(mr.quantity), 2) AS '平均监测数量',
    MIN(mr.monitoring_time) AS '首次监测时间',
    MAX(mr.monitoring_time) AS '最近监测时间',
    ROUND(COUNT(DISTINCT mr.record_id) * 100.0 / 
          (SELECT COUNT(*) FROM monitoring_record 
           WHERE DATE_FORMAT(monitoring_time, '%Y-%m') = DATE_FORMAT(mr.monitoring_time, '%Y-%m')), 2) AS '占当月比例(%)'
FROM monitoring_record mr
GROUP BY DATE_FORMAT(mr.monitoring_time, '%Y-%m'), mr.data_status, mr.monitoring_method
ORDER BY DATE_FORMAT(mr.monitoring_time, '%Y-%m') DESC, mr.data_status;


-- ============================================
-- 2. 生态环境监测业务线视图（3个）
-- ============================================

-- 视图2.1：环境预警汇总视图
DROP VIEW IF EXISTS v_environmental_alert_summary;
CREATE VIEW v_environmental_alert_summary AS
SELECT 
    fa.area_name AS '区域名称',
    fa.area_type AS '区域类型',
    mi.indicator_name AS '监测指标',
    mi.unit AS '单位',
    COUNT(DISTINCT ed.data_id) AS '总监测次数',
    COUNT(DISTINCT CASE WHEN ed.monitoring_value > mi.threshold_upper 
          THEN ed.data_id END) AS '超上限次数',
    COUNT(DISTINCT CASE WHEN ed.monitoring_value < mi.threshold_lower 
          THEN ed.data_id END) AS '低下限次数',
    ROUND(AVG(ed.monitoring_value), 2) AS '平均值',
    MAX(ed.monitoring_value) AS '最大值',
    MIN(ed.monitoring_value) AS '最小值',
    mi.threshold_upper AS '上限阈值',
    mi.threshold_lower AS '下限阈值',
    CASE 
        WHEN COUNT(DISTINCT CASE WHEN ed.monitoring_value > mi.threshold_upper 
             OR ed.monitoring_value < mi.threshold_lower THEN ed.data_id END) > 0 
        THEN '存在异常'
        ELSE '正常'
    END AS '预警状态',
    MAX(ed.collection_time) AS '最近监测时间'
FROM environmental_data ed
INNER JOIN monitoring_indicator mi ON ed.indicator_id = mi.indicator_id
INNER JOIN functional_area fa ON ed.area_id = fa.area_id
WHERE ed.collection_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY fa.area_name, fa.area_type, mi.indicator_name, mi.unit, 
         mi.threshold_upper, mi.threshold_lower
ORDER BY COUNT(DISTINCT CASE WHEN ed.monitoring_value > mi.threshold_upper 
         OR ed.monitoring_value < mi.threshold_lower THEN ed.data_id END) DESC;

-- 视图2.2：设备运行状态视图
DROP VIEW IF EXISTS v_device_operation_status;
CREATE VIEW v_device_operation_status AS
SELECT 
    md.device_id AS '设备编号',
    md.device_type AS '设备类型',
    fa.area_name AS '部署区域',
    fa.area_type AS '区域类型',
    md.installation_date AS '安装日期',
    DATEDIFF(CURDATE(), md.installation_date) AS '使用天数',
    md.calibration_cycle AS '校准周期(天)',
    md.last_calibration_date AS '最后校准日期',
    CASE 
        WHEN md.last_calibration_date IS NULL THEN '从未校准'
        WHEN DATEDIFF(CURDATE(), md.last_calibration_date) > md.calibration_cycle THEN '需要校准'
        ELSE '校准正常'
    END AS '校准状态',
    md.operation_status AS '运行状态',
    md.communication_protocol AS '通信协议',
    COUNT(DISTINCT mr.record_id) AS '监测记录数',
    COUNT(DISTINCT ed.data_id) AS '环境数据记录数',
    MAX(GREATEST(IFNULL(mr.monitoring_time, '1900-01-01'), 
                 IFNULL(ed.collection_time, '1900-01-01'))) AS '最后使用时间',
    CASE 
        WHEN md.operation_status = '故障' THEN '需维修'
        WHEN md.operation_status = '离线' THEN '需检查'
        WHEN DATEDIFF(CURDATE(), IFNULL(md.last_calibration_date, md.installation_date)) > md.calibration_cycle 
        THEN '需校准'
        ELSE '正常'
    END AS '维护建议'
FROM monitoring_device md
INNER JOIN functional_area fa ON md.deployment_area_id = fa.area_id
LEFT JOIN monitoring_record mr ON md.device_id = mr.device_id
LEFT JOIN environmental_data ed ON md.device_id = ed.device_id
GROUP BY md.device_id, md.device_type, fa.area_name, fa.area_type,
         md.installation_date, md.calibration_cycle, md.last_calibration_date,
         md.operation_status, md.communication_protocol
ORDER BY md.operation_status DESC, DATEDIFF(CURDATE(), md.installation_date) DESC;

-- 视图2.3：数据质量统计视图
DROP VIEW IF EXISTS v_data_quality_statistics;
CREATE VIEW v_data_quality_statistics AS
SELECT 
    DATE_FORMAT(ed.collection_time, '%Y-%m') AS '月份',
    fa.area_name AS '区域名称',
    mi.indicator_name AS '监测指标',
    ed.data_quality AS '数据质量',
    COUNT(DISTINCT ed.data_id) AS '数据条数',
    ROUND(AVG(ed.monitoring_value), 2) AS '平均监测值',
    COUNT(DISTINCT ed.device_id) AS '设备数量',
    ROUND(COUNT(DISTINCT ed.data_id) * 100.0 / 
          (SELECT COUNT(*) FROM environmental_data 
           WHERE DATE_FORMAT(collection_time, '%Y-%m') = DATE_FORMAT(ed.collection_time, '%Y-%m')
           AND area_id = ed.area_id), 2) AS '占区域比例(%)',
    CASE ed.data_quality
        WHEN '优' THEN 1
        WHEN '良' THEN 2
        WHEN '中' THEN 3
        WHEN '差' THEN 4
    END AS '质量等级'
FROM environmental_data ed
INNER JOIN functional_area fa ON ed.area_id = fa.area_id
INNER JOIN monitoring_indicator mi ON ed.indicator_id = mi.indicator_id
GROUP BY DATE_FORMAT(ed.collection_time, '%Y-%m'), fa.area_name, 
         mi.indicator_name, ed.data_quality
ORDER BY DATE_FORMAT(ed.collection_time, '%Y-%m') DESC, 
         fa.area_name, 
         CASE ed.data_quality WHEN '优' THEN 1 WHEN '良' THEN 2 WHEN '中' THEN 3 WHEN '差' THEN 4 END;


-- ============================================
-- 3. 游客智能管理业务线视图（3个）
-- ============================================

-- 视图3.1：游客流量分析视图
DROP VIEW IF EXISTS v_visitor_traffic_analysis;
CREATE VIEW v_visitor_traffic_analysis AS
SELECT 
    DATE(v.entry_time) AS '日期',
    DAYNAME(v.entry_time) AS '星期',
    COUNT(DISTINCT v.visitor_id) AS '入园游客数',
    COUNT(DISTINCT CASE WHEN v.exit_time IS NOT NULL THEN v.visitor_id END) AS '已离园数',
    COUNT(DISTINCT CASE WHEN v.exit_time IS NULL THEN v.visitor_id END) AS '在园人数',
    COUNT(DISTINCT CASE WHEN v.entry_method = '线上预约' THEN v.visitor_id END) AS '线上预约数',
    COUNT(DISTINCT CASE WHEN v.entry_method = '现场购票' THEN v.visitor_id END) AS '现场购票数',
    ROUND(AVG(CASE WHEN v.exit_time IS NOT NULL 
              THEN TIMESTAMPDIFF(MINUTE, v.entry_time, v.exit_time) END), 2) AS '平均游览时长(分钟)',
    MIN(v.entry_time) AS '首位入园时间',
    MAX(v.entry_time) AS '末位入园时间',
    HOUR(MIN(v.entry_time)) AS '入园高峰时段开始',
    COUNT(DISTINCT r.reservation_id) AS '预约记录数',
    SUM(r.ticket_amount) AS '当日票款总额'
FROM visitor v
LEFT JOIN reservation r ON v.visitor_id = r.visitor_id 
    AND DATE(r.reservation_date) = DATE(v.entry_time)
WHERE v.entry_time IS NOT NULL
GROUP BY DATE(v.entry_time), DAYNAME(v.entry_time)
ORDER BY DATE(v.entry_time) DESC;

-- 视图3.2：预约统计视图
DROP VIEW IF EXISTS v_reservation_statistics;
CREATE VIEW v_reservation_statistics AS
SELECT 
    r.reservation_date AS '预约日期',
    DAYNAME(r.reservation_date) AS '星期',
    r.entry_time_slot AS '入园时段',
    COUNT(DISTINCT r.reservation_id) AS '预约数量',
    SUM(r.party_size) AS '预约总人数',
    COUNT(DISTINCT CASE WHEN r.reservation_status = '已确认' THEN r.reservation_id END) AS '已确认',
    COUNT(DISTINCT CASE WHEN r.reservation_status = '已取消' THEN r.reservation_id END) AS '已取消',
    COUNT(DISTINCT CASE WHEN r.reservation_status = '已完成' THEN r.reservation_id END) AS '已完成',
    ROUND(COUNT(DISTINCT CASE WHEN r.reservation_status = '已完成' THEN r.reservation_id END) * 100.0 /
          NULLIF(COUNT(DISTINCT r.reservation_id), 0), 2) AS '完成率(%)',
    SUM(CASE WHEN r.payment_status = '已支付' THEN r.ticket_amount ELSE 0 END) AS '已收票款',
    SUM(CASE WHEN r.payment_status = '未支付' THEN r.ticket_amount ELSE 0 END) AS '未收票款',
    ROUND(AVG(r.ticket_amount), 2) AS '平均票款',
    COUNT(DISTINCT r.visitor_id) AS '预约游客数'
FROM reservation r
GROUP BY r.reservation_date, DAYNAME(r.reservation_date), r.entry_time_slot
ORDER BY r.reservation_date DESC, r.entry_time_slot;

-- 视图3.3：区域承载状态视图
DROP VIEW IF EXISTS v_area_capacity_status;
CREATE VIEW v_area_capacity_status AS
SELECT 
    fa.area_id AS '区域编号',
    fa.area_name AS '区域名称',
    fa.area_type AS '区域类型',
    tc.daily_capacity AS '日最大承载量',
    tc.current_visitor_count AS '当前在园人数',
    tc.warning_threshold AS '预警阈值',
    tc.current_status AS '当前状态',
    ROUND(tc.current_visitor_count * 100.0 / tc.daily_capacity, 2) AS '承载率(%)',
    tc.daily_capacity - tc.current_visitor_count AS '剩余容量',
    CASE 
        WHEN tc.current_visitor_count >= tc.daily_capacity THEN '已满载-建议限流'
        WHEN tc.current_visitor_count >= tc.warning_threshold THEN '接近饱和-建议预警'
        WHEN tc.current_visitor_count >= tc.daily_capacity * 0.5 THEN '正常-可接待'
        ELSE '空闲-推荐游览'
    END AS '接待建议',
    COUNT(DISTINCT vt.visitor_id) AS '活跃轨迹游客数',
    COUNT(DISTINCT vt.trajectory_id) AS '轨迹记录数',
    COUNT(DISTINCT CASE WHEN vt.out_of_route = 'Y' THEN vt.visitor_id END) AS '越界游客数',
    CASE 
        WHEN tc.current_status = '限流' THEN '红色'
        WHEN tc.current_status = '预警' THEN '黄色'
        ELSE '绿色'
    END AS '预警等级'
FROM functional_area fa
INNER JOIN traffic_control tc ON fa.area_id = tc.area_id
LEFT JOIN visitor_trajectory vt ON fa.area_id = vt.area_id 
    AND DATE(vt.tracking_time) = CURDATE()
GROUP BY fa.area_id, fa.area_name, fa.area_type, tc.daily_capacity,
         tc.current_visitor_count, tc.warning_threshold, tc.current_status
ORDER BY tc.current_status DESC, 
         ROUND(tc.current_visitor_count * 100.0 / tc.daily_capacity, 2) DESC;


-- ============================================
-- 4. 执法监管业务线视图（3个）
-- ============================================

-- 视图4.1：执法效率分析视图
DROP VIEW IF EXISTS v_enforcement_efficiency;
CREATE VIEW v_enforcement_efficiency AS
SELECT 
    le.enforcer_id AS '执法人员ID',
    le.enforcer_name AS '执法人员',
    le.department AS '所属部门',
    COUNT(DISTINCT ed.dispatch_id) AS '处理案件总数',
    COUNT(DISTINCT CASE WHEN ed.dispatch_status = '已完成' THEN ed.dispatch_id END) AS '已完成案件',
    COUNT(DISTINCT CASE WHEN ed.dispatch_status = '已派单' THEN ed.dispatch_id END) AS '处理中案件',
    COUNT(DISTINCT CASE WHEN ed.dispatch_status = '待响应' THEN ed.dispatch_id END) AS '待响应案件',
    ROUND(COUNT(DISTINCT CASE WHEN ed.dispatch_status = '已完成' THEN ed.dispatch_id END) * 100.0 /
          NULLIF(COUNT(DISTINCT ed.dispatch_id), 0), 2) AS '结案率(%)',
    ROUND(AVG(CASE WHEN ed.response_time IS NOT NULL 
              THEN TIMESTAMPDIFF(MINUTE, ed.dispatch_time, ed.response_time) END), 2) AS '平均响应时间(分钟)',
    ROUND(AVG(CASE WHEN ed.completion_time IS NOT NULL 
              THEN TIMESTAMPDIFF(HOUR, ed.dispatch_time, ed.completion_time) END), 2) AS '平均处置时长(小时)',
    MIN(ed.dispatch_time) AS '首次派单时间',
    MAX(ed.dispatch_time) AS '最近派单时间',
    COUNT(DISTINCT ib.area_id) AS '涉及区域数',
    CASE 
        WHEN COUNT(DISTINCT ed.dispatch_id) >= 50 THEN '工作饱和'
        WHEN COUNT(DISTINCT ed.dispatch_id) >= 20 THEN '工作正常'
        ELSE '工作量较少'
    END AS '工作量评估'
FROM law_enforcer le
LEFT JOIN enforcement_dispatch ed ON le.enforcer_id = ed.enforcer_id
LEFT JOIN illegal_behavior ib ON ed.record_id = ib.record_id
GROUP BY le.enforcer_id, le.enforcer_name, le.department
ORDER BY COUNT(DISTINCT ed.dispatch_id) DESC;

-- 视图4.2：违规行为趋势视图
DROP VIEW IF EXISTS v_illegal_behavior_trends;
CREATE VIEW v_illegal_behavior_trends AS
SELECT 
    DATE_FORMAT(ib.occurrence_time, '%Y-%m') AS '月份',
    ib.behavior_type AS '行为类型',
    fa.area_name AS '发生区域',
    fa.area_type AS '区域类型',
    COUNT(DISTINCT ib.record_id) AS '发生次数',
    COUNT(DISTINCT CASE WHEN ib.handling_status = '已结案' THEN ib.record_id END) AS '已结案',
    COUNT(DISTINCT CASE WHEN ib.handling_status = '处理中' THEN ib.record_id END) AS '处理中',
    COUNT(DISTINCT CASE WHEN ib.handling_status = '未处理' THEN ib.record_id END) AS '未处理',
    ROUND(COUNT(DISTINCT CASE WHEN ib.handling_status = '已结案' THEN ib.record_id END) * 100.0 /
          NULLIF(COUNT(DISTINCT ib.record_id), 0), 2) AS '结案率(%)',
    COUNT(DISTINCT ib.enforcer_id) AS '涉及执法人员数',
    MIN(ib.occurrence_time) AS '首次发生时间',
    MAX(ib.occurrence_time) AS '最近发生时间',
    DATEDIFF(MAX(ib.occurrence_time), MIN(ib.occurrence_time)) + 1 AS '时间跨度(天)',
    ROUND(COUNT(DISTINCT ib.record_id) * 1.0 / 
          NULLIF(DATEDIFF(MAX(ib.occurrence_time), MIN(ib.occurrence_time)) + 1, 0), 2) AS '日均发生频率'
FROM illegal_behavior ib
INNER JOIN functional_area fa ON ib.area_id = fa.area_id
GROUP BY DATE_FORMAT(ib.occurrence_time, '%Y-%m'), ib.behavior_type, 
         fa.area_name, fa.area_type
ORDER BY DATE_FORMAT(ib.occurrence_time, '%Y-%m') DESC, 
         COUNT(DISTINCT ib.record_id) DESC;

-- 视图4.3：执法人员工作量视图
DROP VIEW IF EXISTS v_enforcer_workload;
CREATE VIEW v_enforcer_workload AS
SELECT 
    le.enforcer_name AS '执法人员',
    le.department AS '所属部门',
    le.enforcement_authority AS '执法权限',
    DATE_FORMAT(ed.dispatch_time, '%Y-%m') AS '月份',
    COUNT(DISTINCT ed.dispatch_id) AS '派单总数',
    COUNT(DISTINCT CASE WHEN ed.dispatch_status = '已完成' THEN ed.dispatch_id END) AS '完成数',
    COUNT(DISTINCT CASE WHEN ed.dispatch_status = '已派单' THEN ed.dispatch_id END) AS '进行中',
    COUNT(DISTINCT CASE WHEN ed.dispatch_status = '待响应' THEN ed.dispatch_id END) AS '待响应',
    COUNT(DISTINCT ib.area_id) AS '覆盖区域数',
    COUNT(DISTINCT ib.behavior_type) AS '处理行为类型数',
    ROUND(AVG(TIMESTAMPDIFF(MINUTE, ed.dispatch_time, ed.response_time)), 2) AS '平均响应时间(分钟)',
    ROUND(AVG(TIMESTAMPDIFF(HOUR, ed.response_time, ed.completion_time)), 2) AS '平均处理时长(小时)',
    SUM(TIMESTAMPDIFF(HOUR, ed.dispatch_time, IFNULL(ed.completion_time, NOW()))) AS '累计工作时长(小时)',
    CASE 
        WHEN COUNT(DISTINCT ed.dispatch_id) > 30 THEN '高负荷'
        WHEN COUNT(DISTINCT ed.dispatch_id) > 15 THEN '正常'
        ELSE '低负荷'
    END AS '负荷状态'
FROM law_enforcer le
LEFT JOIN enforcement_dispatch ed ON le.enforcer_id = ed.enforcer_id
LEFT JOIN illegal_behavior ib ON ed.record_id = ib.record_id
WHERE ed.dispatch_time >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY le.enforcer_name, le.department, le.enforcement_authority,
         DATE_FORMAT(ed.dispatch_time, '%Y-%m')
ORDER BY DATE_FORMAT(ed.dispatch_time, '%Y-%m') DESC, 
         COUNT(DISTINCT ed.dispatch_id) DESC;


-- ============================================
-- 5. 科研数据支撑业务线视图（3个）
-- ============================================

-- 视图5.1：项目进展总览视图
DROP VIEW IF EXISTS v_project_progress_overview;
CREATE VIEW v_project_progress_overview AS
SELECT 
    rp.project_id AS '项目编号',
    rp.project_name AS '项目名称',
    su.real_name AS '项目负责人',
    rp.applicant_unit AS '申请单位',
    rp.research_field AS '研究领域',
    rp.project_status AS '项目状态',
    rp.start_date AS '立项日期',
    rp.end_date AS '结题日期',
    DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date) AS '项目天数',
    COUNT(DISTINCT rdc.collection_id) AS '数据采集次数',
    COUNT(DISTINCT rdc.area_id) AS '涉及区域数',
    COUNT(DISTINCT rdc.collector_id) AS '参与人员数',
    COUNT(DISTINCT ra.achievement_id) AS '产出成果数',
    COUNT(DISTINCT CASE WHEN ra.achievement_type = '论文' THEN ra.achievement_id END) AS '论文数',
    COUNT(DISTINCT CASE WHEN ra.achievement_type = '报告' THEN ra.achievement_id END) AS '报告数',
    COUNT(DISTINCT CASE WHEN ra.achievement_type = '专利' THEN ra.achievement_id END) AS '专利数',
    ROUND(COUNT(DISTINCT ra.achievement_id) * 1.0 / 
          NULLIF(DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date), 0) * 365, 2) AS '年均成果产出',
    CASE 
        WHEN rp.project_status = '已结题' THEN '已完成'
        WHEN DATEDIFF(CURDATE(), rp.start_date) > 730 THEN '长期项目'
        WHEN DATEDIFF(CURDATE(), rp.start_date) > 365 THEN '中期项目'
        ELSE '新项目'
    END AS '项目阶段'
FROM research_project rp
INNER JOIN system_user su ON rp.principal_id = su.user_id
LEFT JOIN research_data_collection rdc ON rp.project_id = rdc.project_id
LEFT JOIN research_achievement ra ON rp.project_id = ra.project_id
GROUP BY rp.project_id, rp.project_name, su.real_name, rp.applicant_unit,
         rp.research_field, rp.project_status, rp.start_date, rp.end_date
ORDER BY rp.project_status, rp.start_date DESC;

-- 视图5.2：科研成果统计视图
DROP VIEW IF EXISTS v_research_achievement_statistics;
CREATE VIEW v_research_achievement_statistics AS
SELECT 
    rp.research_field AS '研究领域',
    DATE_FORMAT(ra.publish_date, '%Y') AS '发表年份',
    ra.achievement_type AS '成果类型',
    COUNT(DISTINCT ra.achievement_id) AS '成果数量',
    COUNT(DISTINCT rp.project_id) AS '涉及项目数',
    COUNT(DISTINCT rp.principal_id) AS '参与研究人员数',
    COUNT(DISTINCT CASE WHEN ra.share_permission = '公开' THEN ra.achievement_id END) AS '公开成果数',
    COUNT(DISTINCT CASE WHEN ra.share_permission = '内部共享' THEN ra.achievement_id END) AS '内部共享数',
    COUNT(DISTINCT CASE WHEN ra.share_permission = '保密' THEN ra.achievement_id END) AS '保密成果数',
    ROUND(COUNT(DISTINCT CASE WHEN ra.share_permission = '公开' THEN ra.achievement_id END) * 100.0 /
          NULLIF(COUNT(DISTINCT ra.achievement_id), 0), 2) AS '公开率(%)',
    MIN(ra.publish_date) AS '首个成果日期',
    MAX(ra.publish_date) AS '最新成果日期',
    GROUP_CONCAT(DISTINCT rp.project_name ORDER BY ra.publish_date DESC SEPARATOR '；') AS '相关项目'
FROM research_achievement ra
INNER JOIN research_project rp ON ra.project_id = rp.project_id
GROUP BY rp.research_field, DATE_FORMAT(ra.publish_date, '%Y'), ra.achievement_type
ORDER BY DATE_FORMAT(ra.publish_date, '%Y') DESC, 
         rp.research_field, 
         COUNT(DISTINCT ra.achievement_id) DESC;

-- 视图5.3：数据采集汇总视图
DROP VIEW IF EXISTS v_data_collection_summary;
CREATE VIEW v_data_collection_summary AS
SELECT 
    DATE_FORMAT(rdc.collection_time, '%Y-%m') AS '月份',
    rp.project_name AS '项目名称',
    rp.research_field AS '研究领域',
    fa.area_name AS '采集区域',
    fa.area_type AS '区域类型',
    rdc.data_source AS '数据来源',
    COUNT(DISTINCT rdc.collection_id) AS '采集次数',
    COUNT(DISTINCT rdc.collector_id) AS '采集人员数',
    COUNT(DISTINCT rdc.sample_number) AS '样本数量',
    MIN(rdc.collection_time) AS '首次采集时间',
    MAX(rdc.collection_time) AS '最近采集时间',
    DATEDIFF(MAX(rdc.collection_time), MIN(rdc.collection_time)) + 1 AS '采集时间跨度(天)',
    ROUND(COUNT(DISTINCT rdc.collection_id) * 1.0 / 
          NULLIF(DATEDIFF(MAX(rdc.collection_time), MIN(rdc.collection_time)) + 1, 0), 2) AS '日均采集频率',
    CASE 
        WHEN COUNT(DISTINCT rdc.collection_id) >= 50 THEN '高频采集'
        WHEN COUNT(DISTINCT rdc.collection_id) >= 20 THEN '正常采集'
        ELSE '低频采集'
    END AS '采集强度'
FROM research_data_collection rdc
INNER JOIN research_project rp ON rdc.project_id = rp.project_id
INNER JOIN functional_area fa ON rdc.area_id = fa.area_id
GROUP BY DATE_FORMAT(rdc.collection_time, '%Y-%m'), rp.project_name, 
         rp.research_field, fa.area_name, fa.area_type, rdc.data_source
ORDER BY DATE_FORMAT(rdc.collection_time, '%Y-%m') DESC, 
         COUNT(DISTINCT rdc.collection_id) DESC;
-- ============================================
-- 超额完成：额外5个高级分析视图
-- ============================================

-- 超额视图1：跨业务线综合分析视图 - 生态健康指数
DROP VIEW IF EXISTS v_ecological_health_index;
CREATE VIEW v_ecological_health_index AS
SELECT 
    fa.area_id AS '区域编号',
    fa.area_name AS '区域名称',
    fa.area_type AS '区域类型',
    -- 生物多样性得分（40分）
    ROUND(LEAST(COUNT(DISTINCT mr.species_id) * 2, 40), 1) AS '物种多样性得分',
    -- 环境质量得分（30分）
    ROUND(COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良') 
          THEN ed.data_id END) * 30.0 / 
          NULLIF(COUNT(DISTINCT ed.data_id), 0), 1) AS '环境质量得分',
    -- 人为干扰得分（30分，越少越好）
    ROUND(30 - LEAST(COUNT(DISTINCT ib.record_id) * 3, 30), 1) AS '人为干扰得分',
    -- 综合健康指数
    ROUND(
        LEAST(COUNT(DISTINCT mr.species_id) * 2, 40) +
        COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良') 
              THEN ed.data_id END) * 30.0 / 
              NULLIF(COUNT(DISTINCT ed.data_id), 0) +
        30 - LEAST(COUNT(DISTINCT ib.record_id) * 3, 30),
    1) AS '生态健康指数',
    CASE 
        WHEN ROUND(
            LEAST(COUNT(DISTINCT mr.species_id) * 2, 40) +
            COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良') 
                  THEN ed.data_id END) * 30.0 / 
                  NULLIF(COUNT(DISTINCT ed.data_id), 0) +
            30 - LEAST(COUNT(DISTINCT ib.record_id) * 3, 30),
        1) >= 85 THEN '优秀'
        WHEN ROUND(
            LEAST(COUNT(DISTINCT mr.species_id) * 2, 40) +
            COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良') 
                  THEN ed.data_id END) * 30.0 / 
                  NULLIF(COUNT(DISTINCT ed.data_id), 0) +
            30 - LEAST(COUNT(DISTINCT ib.record_id) * 3, 30),
        1) >= 70 THEN '良好'
        WHEN ROUND(
            LEAST(COUNT(DISTINCT mr.species_id) * 2, 40) +
            COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良') 
                  THEN ed.data_id END) * 30.0 / 
                  NULLIF(COUNT(DISTINCT ed.data_id), 0) +
            30 - LEAST(COUNT(DISTINCT ib.record_id) * 3, 30),
        1) >= 60 THEN '中等'
        ELSE '需改善'
    END AS '健康等级',
    COUNT(DISTINCT mr.species_id) AS '物种数量',
    COUNT(DISTINCT ed.data_id) AS '环境监测次数',
    COUNT(DISTINCT ib.record_id) AS '违规事件数',
    COUNT(DISTINCT v.visitor_id) AS '游客访问数'
FROM functional_area fa
LEFT JOIN monitoring_record mr ON fa.area_id = 
    (SELECT area_id FROM monitoring_device WHERE device_id = mr.device_id)
LEFT JOIN environmental_data ed ON fa.area_id = ed.area_id
LEFT JOIN illegal_behavior ib ON fa.area_id = ib.area_id
LEFT JOIN visitor_trajectory vt ON fa.area_id = vt.area_id
LEFT JOIN visitor v ON vt.visitor_id = v.visitor_id
WHERE mr.monitoring_time >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
  AND ed.collection_time >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
  AND ib.occurrence_time >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
GROUP BY fa.area_id, fa.area_name, fa.area_type
ORDER BY ROUND(
    LEAST(COUNT(DISTINCT mr.species_id) * 2, 40) +
    COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良') 
          THEN ed.data_id END) * 30.0 / 
          NULLIF(COUNT(DISTINCT ed.data_id), 0) +
    30 - LEAST(COUNT(DISTINCT ib.record_id) * 3, 30),
1) DESC;


-- 超额视图2：用户活跃度分析视图（RBAC相关）
DROP VIEW IF EXISTS v_user_activity_analysis;
CREATE VIEW v_user_activity_analysis AS
SELECT 
    su.user_id AS '用户ID',
    su.real_name AS '姓名',
    su.role_type AS '角色',
    su.account_status AS '账号状态',
    su.create_time AS '注册时间',
    su.last_login_time AS '最后登录',
    DATEDIFF(CURDATE(), su.create_time) AS '账号使用天数',
    DATEDIFF(CURDATE(), su.last_login_time) AS '未登录天数',
    -- 统计各种操作记录
    COUNT(DISTINCT mr.record_id) AS '监测记录数',
    COUNT(DISTINCT rdc.collection_id) AS '科研采集数',
    COUNT(DISTINCT rp.project_id) AS '负责项目数',
    COUNT(DISTINCT ed_dispatch.dispatch_id) AS '执法派单数',
    COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT rdc.collection_id) + 
    COUNT(DISTINCT rp.project_id) + COUNT(DISTINCT ed_dispatch.dispatch_id) AS '总操作数',
    CASE 
        WHEN su.last_login_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) THEN '活跃'
        WHEN su.last_login_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN '一般'
        WHEN su.last_login_time >= DATE_SUB(CURDATE(), INTERVAL 90 DAY) THEN '不活跃'
        ELSE '沉默'
    END AS '活跃度',
    CASE su.role_type
        WHEN '生态监测员' THEN '可查看监测数据、录入监测记录'
        WHEN '数据分析师' THEN '可查看所有统计视图、生成分析报告'
        WHEN '执法人员' THEN '可处理违规行为、查看执法记录'
        WHEN '科研人员' THEN '可采集科研数据、管理科研项目'
        WHEN '系统管理员' THEN '全部权限'
        ELSE '基础查看权限'
    END AS '权限范围'
FROM system_user su
LEFT JOIN monitoring_record mr ON su.user_id = mr.recorder_id
LEFT JOIN research_data_collection rdc ON su.user_id = rdc.collector_id
LEFT JOIN research_project rp ON su.user_id = rp.principal_id
LEFT JOIN enforcement_dispatch ed_dispatch ON su.user_id = 
    (SELECT enforcer_id FROM law_enforcer WHERE enforcer_id = ed_dispatch.enforcer_id LIMIT 1)
GROUP BY su.user_id, su.real_name, su.role_type, su.account_status, 
         su.create_time, su.last_login_time
ORDER BY su.last_login_time DESC;


-- 超额视图3：设备投资回报率分析视图
DROP VIEW IF EXISTS v_device_roi_analysis;
CREATE VIEW v_device_roi_analysis AS
SELECT 
    md.device_id AS '设备编号',
    md.device_type AS '设备类型',
    fa.area_name AS '部署区域',
    md.installation_date AS '安装日期',
    DATEDIFF(CURDATE(), md.installation_date) AS '使用天数',
    -- 假设每台设备成本5万元，每次数据价值50元
    50000 AS '设备成本(元)',
    COUNT(DISTINCT mr.record_id) AS '生物监测次数',
    COUNT(DISTINCT ed.data_id) AS '环境数据次数',
    (COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 50 AS '累计产出价值(元)',
    ROUND((COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 50.0 / 50000 * 100, 2) AS '投资回报率(%)',
    ROUND((COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 1.0 / 
          NULLIF(DATEDIFF(CURDATE(), md.installation_date), 0), 2) AS '日均数据产出',
    CASE 
        WHEN md.operation_status = '故障' THEN 0
        WHEN (COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 50.0 / 50000 >= 1 THEN '已回本'
        WHEN (COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 50.0 / 50000 >= 0.5 THEN '接近回本'
        ELSE '投入期'
    END AS '投资状态',
    CASE 
        WHEN md.operation_status = '故障' THEN '需维修'
        WHEN (COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) = 0 THEN '未启用'
        WHEN ROUND((COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 1.0 / 
             NULLIF(DATEDIFF(CURDATE(), md.installation_date), 0), 2) < 0.5 THEN '利用率低'
        ELSE '正常使用'
    END AS '使用评估'
FROM monitoring_device md
INNER JOIN functional_area fa ON md.deployment_area_id = fa.area_id
LEFT JOIN monitoring_record mr ON md.device_id = mr.device_id
LEFT JOIN environmental_data ed ON md.device_id = ed.device_id
GROUP BY md.device_id, md.device_type, fa.area_name, md.installation_date, md.operation_status
ORDER BY (COUNT(DISTINCT mr.record_id) + COUNT(DISTINCT ed.data_id)) * 50.0 / 50000 DESC;


-- 超额视图4：季节性生态变化趋势视图
DROP VIEW IF EXISTS v_seasonal_ecology_trends;
CREATE VIEW v_seasonal_ecology_trends AS
SELECT 
    YEAR(mr.monitoring_time) AS '年份',
    QUARTER(mr.monitoring_time) AS '季度',
    CASE QUARTER(mr.monitoring_time)
        WHEN 1 THEN '春季(1-3月)'
        WHEN 2 THEN '夏季(4-6月)'
        WHEN 3 THEN '秋季(7-9月)'
        WHEN 4 THEN '冬季(10-12月)'
    END AS '季节',
    COUNT(DISTINCT mr.species_id) AS '观测物种数',
    COUNT(DISTINCT mr.record_id) AS '监测记录数',
    SUM(mr.quantity) AS '累计观测个体数',
    ROUND(AVG(mr.quantity), 2) AS '平均种群数量',
    COUNT(DISTINCT CASE WHEN s.protection_level = '国家一级' 
          THEN mr.species_id END) AS '一级保护物种数',
    COUNT(DISTINCT CASE WHEN s.protection_level = '国家二级' 
          THEN mr.species_id END) AS '二级保护物种数',
    -- 环境数据
    ROUND(AVG(CASE WHEN mi.indicator_name = '温度' 
              THEN ed.monitoring_value END), 2) AS '平均温度',
    ROUND(AVG(CASE WHEN mi.indicator_name = '湿度' 
              THEN ed.monitoring_value END), 2) AS '平均湿度',
    ROUND(AVG(CASE WHEN mi.indicator_name LIKE '%降水%' 
              THEN ed.monitoring_value END), 2) AS '平均降水量',
    -- 游客影响
    COUNT(DISTINCT v.visitor_id) AS '游客访问量',
    COUNT(DISTINCT ib.record_id) AS '违规事件数',
    -- 季节特征
    CASE 
        WHEN QUARTER(mr.monitoring_time) IN (2, 3) THEN '生态活跃期'
        WHEN QUARTER(mr.monitoring_time) = 1 THEN '生态恢复期'
        ELSE '生态休眠期'
    END AS '生态周期'
FROM monitoring_record mr
INNER JOIN species s ON mr.species_id = s.species_id
LEFT JOIN environmental_data ed ON DATE(mr.monitoring_time) = DATE(ed.collection_time)
LEFT JOIN monitoring_indicator mi ON ed.indicator_id = mi.indicator_id
LEFT JOIN visitor_trajectory vt ON DATE(mr.monitoring_time) = DATE(vt.tracking_time)
LEFT JOIN visitor v ON vt.visitor_id = v.visitor_id
LEFT JOIN illegal_behavior ib ON DATE(mr.monitoring_time) = DATE(ib.occurrence_time)
WHERE mr.monitoring_time >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
GROUP BY YEAR(mr.monitoring_time), QUARTER(mr.monitoring_time)
ORDER BY YEAR(mr.monitoring_time) DESC, QUARTER(mr.monitoring_time) DESC;


-- 超额视图5：科研-保护协同效果评估视图
DROP VIEW IF EXISTS v_research_conservation_synergy;
CREATE VIEW v_research_conservation_synergy AS
SELECT 
    rp.project_id AS '项目编号',
    rp.project_name AS '项目名称',
    rp.research_field AS '研究领域',
    su.real_name AS '项目负责人',
    -- 科研投入
    COUNT(DISTINCT rdc.collection_id) AS '数据采集次数',
    COUNT(DISTINCT ra.achievement_id) AS '产出成果数',
    DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date) AS '研究天数',
    -- 保护成效（研究区域的生态改善）
    COUNT(DISTINCT mr.species_id) AS '研究区物种数',
    COUNT(DISTINCT CASE WHEN s.protection_level IN ('国家一级', '国家二级')
          THEN mr.species_id END) AS '保护物种数',
    ROUND(AVG(ed.monitoring_value), 2) AS '环境指标均值',
    COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良')
          THEN ed.data_id END) AS '优质数据量',
    -- 协同效果评分
    ROUND(
        (COUNT(DISTINCT ra.achievement_id) * 10 +  -- 成果产出权重
         COUNT(DISTINCT mr.species_id) * 5 +        -- 物种发现权重
         COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良')
               THEN ed.data_id END) * 0.1) / 
        NULLIF(DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date), 0) * 365,
    2) AS '年度协同得分',
    CASE 
        WHEN ROUND(
            (COUNT(DISTINCT ra.achievement_id) * 10 + 
             COUNT(DISTINCT mr.species_id) * 5 + 
             COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良')
                   THEN ed.data_id END) * 0.1) / 
            NULLIF(DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date), 0) * 365,
        2) >= 100 THEN '卓越'
        WHEN ROUND(
            (COUNT(DISTINCT ra.achievement_id) * 10 + 
             COUNT(DISTINCT mr.species_id) * 5 + 
             COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良')
                   THEN ed.data_id END) * 0.1) / 
            NULLIF(DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date), 0) * 365,
        2) >= 50 THEN '优秀'
        WHEN ROUND(
            (COUNT(DISTINCT ra.achievement_id) * 10 + 
             COUNT(DISTINCT mr.species_id) * 5 + 
             COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良')
                   THEN ed.data_id END) * 0.1) / 
            NULLIF(DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date), 0) * 365,
        2) >= 20 THEN '良好'
        ELSE '一般'
    END AS '协同等级',
    GROUP_CONCAT(DISTINCT fa.area_name ORDER BY fa.area_name SEPARATOR '、') AS '研究区域'
FROM research_project rp
INNER JOIN system_user su ON rp.principal_id = su.user_id
LEFT JOIN research_data_collection rdc ON rp.project_id = rdc.project_id
LEFT JOIN research_achievement ra ON rp.project_id = ra.project_id
LEFT JOIN functional_area fa ON rdc.area_id = fa.area_id
LEFT JOIN monitoring_record mr ON rdc.area_id = 
    (SELECT deployment_area_id FROM monitoring_device WHERE device_id = mr.device_id LIMIT 1)
LEFT JOIN species s ON mr.species_id = s.species_id
LEFT JOIN environmental_data ed ON rdc.area_id = ed.area_id 
    AND DATE(rdc.collection_time) = DATE(ed.collection_time)
GROUP BY rp.project_id, rp.project_name, rp.research_field, su.real_name,
         rp.start_date, rp.end_date
ORDER BY ROUND(
    (COUNT(DISTINCT ra.achievement_id) * 10 + 
     COUNT(DISTINCT mr.species_id) * 5 + 
     COUNT(DISTINCT CASE WHEN ed.data_quality IN ('优', '良')
           THEN ed.data_id END) * 0.1) / 
    NULLIF(DATEDIFF(IFNULL(rp.end_date, CURDATE()), rp.start_date), 0) * 365,
2) DESC;
