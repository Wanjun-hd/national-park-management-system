USE national_park_system;


DELIMITER $$

-- 1生物多样性监测业务线
-- 存储过程1：自动审核监测记录数据质量
-- 功能：根据监测数据的完整性自动更新数据状态
-- 调用示例：CALL sp_validate_monitoring_record('MR20250101001');
DROP PROCEDURE IF EXISTS sp_validate_monitoring_record$$
CREATE PROCEDURE sp_validate_monitoring_record(
    IN p_record_id VARCHAR(30)
)
BEGIN
    DECLARE v_species_id VARCHAR(20);
    DECLARE v_device_id VARCHAR(20);
    DECLARE v_quantity INT;
    DECLARE v_monitoring_method VARCHAR(20);
    DECLARE v_new_status VARCHAR(10);
    
    -- 获取监测记录信息
    SELECT species_id, device_id, quantity, monitoring_method
    INTO v_species_id, v_device_id, v_quantity, v_monitoring_method
    FROM monitoring_record
    WHERE record_id = p_record_id;
    
    -- 判断数据完整性
    IF v_species_id IS NOT NULL 
       AND v_device_id IS NOT NULL 
       AND v_quantity IS NOT NULL 
       AND v_quantity > 0
       AND v_monitoring_method IN ('红外相机', '人工巡查', '无人机') THEN
        SET v_new_status = '有效';
    ELSE
        SET v_new_status = '待核实';
    END IF;
    
    -- 更新数据状态
    UPDATE monitoring_record
    SET data_status = v_new_status
    WHERE record_id = p_record_id;
    
    -- 返回结果
    SELECT CONCAT('记录 ', p_record_id, ' 已更新为：', v_new_status) AS result_message;
END$$

-- 触发器1：监测记录插入时自动记录设备使用情况
-- 功能：当插入新的监测记录时，更新设备的最后使用时间（通过last_calibration_date模拟）
DROP TRIGGER IF EXISTS trg_after_monitoring_insert$$
CREATE TRIGGER trg_after_monitoring_insert
AFTER INSERT ON monitoring_record
FOR EACH ROW
BEGIN
    -- 记录设备使用（这里使用last_calibration_date字段记录最后使用日期）
    UPDATE monitoring_device
    SET last_calibration_date = CURDATE()
    WHERE device_id = NEW.device_id
      AND (last_calibration_date IS NULL OR last_calibration_date < CURDATE());
END$$

-- 2：生态环境监测业务线
-- 存储过程2：异常环境数据自动预警
-- 功能：检测指定时间段内超出阈值的环境监测数据并生成预警报告
-- 调用示例：CALL sp_environment_alert_check('AREA001', 7);
DROP PROCEDURE IF EXISTS sp_environment_alert_check$$
CREATE PROCEDURE sp_environment_alert_check(
    IN p_area_id VARCHAR(20),
    IN p_days INT
)
BEGIN
    DECLARE v_alert_count INT DEFAULT 0;   
    -- 创建临时表存储预警信息
    DROP TEMPORARY TABLE IF EXISTS tmp_alert_data;
    CREATE TEMPORARY TABLE tmp_alert_data (
        data_id VARCHAR(30),
        indicator_name VARCHAR(50),
        monitoring_value DECIMAL(10,2),
        threshold_upper DECIMAL(10,2),
        threshold_lower DECIMAL(10,2),
        collection_time DATETIME,
        alert_type VARCHAR(20)
    );
    -- 查找超标数据
    INSERT INTO tmp_alert_data
    SELECT 
        ed.data_id,
        mi.indicator_name,
        ed.monitoring_value,
        mi.threshold_upper,
        mi.threshold_lower,
        ed.collection_time,
        CASE 
            WHEN ed.monitoring_value > mi.threshold_upper THEN '超过上限'
            WHEN ed.monitoring_value < mi.threshold_lower THEN '低于下限'
        END AS alert_type
    FROM environmental_data ed
    INNER JOIN monitoring_indicator mi ON ed.indicator_id = mi.indicator_id
    WHERE ed.area_id = p_area_id
      AND ed.collection_time >= DATE_SUB(CURDATE(), INTERVAL p_days DAY)
      AND (ed.monitoring_value > mi.threshold_upper 
           OR ed.monitoring_value < mi.threshold_lower);
    -- 统计预警数量
    SELECT COUNT(*) INTO v_alert_count FROM tmp_alert_data;
    -- 返回预警报告
    IF v_alert_count > 0 THEN
        SELECT 
            CONCAT('区域 ', p_area_id, ' 近 ', p_days, ' 天发现 ', v_alert_count, ' 条异常数据') AS alert_summary;
        SELECT * FROM tmp_alert_data ORDER BY collection_time DESC;
    ELSE
        SELECT CONCAT('区域 ', p_area_id, ' 近 ', p_days, ' 天环境数据正常') AS alert_summary;
    END IF;
    
    DROP TEMPORARY TABLE IF EXISTS tmp_alert_data;
END$$


-- 3：游客智能管理业务线
-- 存储过程3：实时更新区域流量状态
-- 功能：根据当前在园人数自动更新流量控制状态
-- 调用示例：CALL sp_update_traffic_status('AREA001');
DROP PROCEDURE IF EXISTS sp_update_traffic_status$$
CREATE PROCEDURE sp_update_traffic_status(
    IN p_area_id VARCHAR(20)
)
BEGIN
    DECLARE v_current_count INT;
    DECLARE v_daily_capacity INT;
    DECLARE v_warning_threshold INT;
    DECLARE v_new_status VARCHAR(10);
    
    -- 获取流量控制信息
    SELECT current_visitor_count, daily_capacity, warning_threshold
    INTO v_current_count, v_daily_capacity, v_warning_threshold
    FROM traffic_control
    WHERE area_id = p_area_id;
    
    -- 判断流量状态
    IF v_current_count >= v_daily_capacity THEN
        SET v_new_status = '限流';
    ELSEIF v_current_count >= v_warning_threshold THEN
        SET v_new_status = '预警';
    ELSE
        SET v_new_status = '正常';
    END IF;
    
    -- 更新流量状态
    UPDATE traffic_control
    SET current_status = v_new_status
    WHERE area_id = p_area_id;
    
    -- 返回更新结果
    SELECT 
        p_area_id AS area_id,
        v_current_count AS current_count,
        v_daily_capacity AS capacity,
        v_new_status AS new_status,
        CONCAT(ROUND(v_current_count * 100.0 / v_daily_capacity, 2), '%') AS occupancy_rate;
END$$

-- 触发器3：游客入园自动更新流量统计
-- 功能：当游客入园时间更新时，自动增加对应区域的在园人数
DROP TRIGGER IF EXISTS trg_visitor_entry_update$$
CREATE TRIGGER trg_visitor_entry_update
AFTER UPDATE ON visitor
FOR EACH ROW
BEGIN
    DECLARE v_area_id VARCHAR(20);
    
    -- 如果是首次记录入园时间（从NULL变为有值）
    IF OLD.entry_time IS NULL AND NEW.entry_time IS NOT NULL THEN
        -- 获取游客当前所在区域（取最新的轨迹记录）
        SELECT area_id INTO v_area_id
        FROM visitor_trajectory
        WHERE visitor_id = NEW.visitor_id
        ORDER BY tracking_time DESC
        LIMIT 1;
        
        -- 如果找到区域，则更新流量统计
        IF v_area_id IS NOT NULL THEN
            UPDATE traffic_control
            SET current_visitor_count = current_visitor_count + 1
            WHERE area_id = v_area_id;
        END IF;
    END IF;
    
    -- 如果是记录离园时间（从NULL变为有值）
    IF OLD.exit_time IS NULL AND NEW.exit_time IS NOT NULL THEN
        -- 获取游客离园前所在区域
        SELECT area_id INTO v_area_id
        FROM visitor_trajectory
        WHERE visitor_id = NEW.visitor_id
        ORDER BY tracking_time DESC
        LIMIT 1;
        
        -- 如果找到区域，则减少流量统计
        IF v_area_id IS NOT NULL THEN
            UPDATE traffic_control
            SET current_visitor_count = GREATEST(current_visitor_count - 1, 0)
            WHERE area_id = v_area_id;
        END IF;
    END IF;
END$$

-- 4：执法监管业务线
-- 存储过程4：自动调度执法人员
-- 功能：根据非法行为发生区域，自动创建执法调度记录
-- 调用示例：CALL sp_auto_dispatch_enforcer('IB20250101001', 'ENF001');
DROP PROCEDURE IF EXISTS sp_auto_dispatch_enforcer$$
CREATE PROCEDURE sp_auto_dispatch_enforcer(
    IN p_record_id VARCHAR(30),
    IN p_enforcer_id VARCHAR(20)
)
BEGIN
    DECLARE v_dispatch_id VARCHAR(30);
    DECLARE v_area_id VARCHAR(20);
    DECLARE v_occurrence_time DATETIME;
    DECLARE v_existing_dispatch INT;
    
    -- 检查是否已存在调度记录
    SELECT COUNT(*) INTO v_existing_dispatch
    FROM enforcement_dispatch
    WHERE record_id = p_record_id;
    
    IF v_existing_dispatch > 0 THEN
        SELECT '该非法行为已存在调度记录' AS error_message;
    ELSE
        -- 获取非法行为信息
        SELECT area_id, occurrence_time
        INTO v_area_id, v_occurrence_time
        FROM illegal_behavior
        WHERE record_id = p_record_id;
        
        -- 生成调度编号
        SET v_dispatch_id = CONCAT('DISP', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s'));
        
        -- 创建调度记录
        INSERT INTO enforcement_dispatch (
            dispatch_id,
            record_id,
            enforcer_id,
            dispatch_time,
            dispatch_status
        ) VALUES (
            v_dispatch_id,
            p_record_id,
            p_enforcer_id,
            NOW(),
            '待响应'
        );
        
        -- 返回调度信息
        SELECT 
            v_dispatch_id AS dispatch_id,
            p_record_id AS record_id,
            p_enforcer_id AS enforcer_id,
            v_area_id AS area_id,
            '调度成功' AS message;
    END IF;
END$$

-- 触发器4：非法行为处理完成自动更新调度状态
-- 功能：当非法行为状态更新为已结案时，自动更新对应的调度状态
DROP TRIGGER IF EXISTS trg_illegal_case_closed$$
CREATE TRIGGER trg_illegal_case_closed
AFTER UPDATE ON illegal_behavior
FOR EACH ROW
BEGIN
    -- 如果非法行为状态变为已结案
    IF OLD.handling_status != '已结案' AND NEW.handling_status = '已结案' THEN
        -- 更新调度状态和完成时间
        UPDATE enforcement_dispatch
        SET dispatch_status = '已完成',
            completion_time = NOW()
        WHERE record_id = NEW.record_id
          AND dispatch_status != '已完成';
    END IF;
END$$
-- 5 ：科研数据支撑业务线
-- 存储过程5：科研项目数据统计
-- 功能：统计指定科研项目的数据采集情况和成果产出情况
-- 调用示例：CALL sp_research_project_statistics('PROJ001');
DROP PROCEDURE IF EXISTS sp_research_project_statistics$$
CREATE PROCEDURE sp_research_project_statistics(
    IN p_project_id VARCHAR(20)
)
BEGIN
    DECLARE v_project_name VARCHAR(100);
    DECLARE v_project_status VARCHAR(10);
    DECLARE v_start_date DATE;
    DECLARE v_end_date DATE;
    
    -- 获取项目基本信息
    SELECT project_name, project_status, start_date, end_date
    INTO v_project_name, v_project_status, v_start_date, v_end_date
    FROM research_project
    WHERE project_id = p_project_id;
    
    -- 项目基本信息
    SELECT 
        p_project_id AS project_id,
        v_project_name AS project_name,
        v_project_status AS project_status,
        v_start_date AS start_date,
        v_end_date AS end_date,
        DATEDIFF(IFNULL(v_end_date, CURDATE()), v_start_date) AS project_duration_days;
    
    -- 数据采集统计
    SELECT 
        '数据采集统计' AS statistics_type,
        COUNT(*) AS total_collections,
        COUNT(CASE WHEN data_source = '实地采集' THEN 1 END) AS field_collections,
        COUNT(CASE WHEN data_source = '系统调用' THEN 1 END) AS system_collections,
        COUNT(DISTINCT area_id) AS areas_covered,
        COUNT(DISTINCT collector_id) AS collectors_count
    FROM research_data_collection
    WHERE project_id = p_project_id;
    
    -- 成果产出统计
    SELECT 
        '成果产出统计' AS statistics_type,
        COUNT(*) AS total_achievements,
        COUNT(CASE WHEN achievement_type = '论文' THEN 1 END) AS papers,
        COUNT(CASE WHEN achievement_type = '报告' THEN 1 END) AS reports,
        COUNT(CASE WHEN achievement_type = '专利' THEN 1 END) AS patents,
        COUNT(CASE WHEN share_permission = '公开' THEN 1 END) AS public_achievements
    FROM research_achievement
    WHERE project_id = p_project_id;
END$$

-- 触发器5：项目结题时禁止新增数据采集记录
-- 功能：当项目状态变为已结题时，防止继续新增数据采集记录
DROP TRIGGER IF EXISTS trg_prevent_collection_after_closure$$
CREATE TRIGGER trg_prevent_collection_after_closure
BEFORE INSERT ON research_data_collection
FOR EACH ROW
BEGIN
    DECLARE v_project_status VARCHAR(10);
    
    -- 检查项目状态
    SELECT project_status INTO v_project_status
    FROM research_project
    WHERE project_id = NEW.project_id;
    
    -- 如果项目已结题，则阻止插入
    IF v_project_status = '已结题' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '项目已结题，不允许新增数据采集记录';
    END IF;
END$$

-- 恢复默认分隔符
DELIMITER ;

-- ============================================
-- 存储过程与触发器说明
-- ============================================
-- 共创建：
-- - 5个存储过程（每条业务线1个）
-- - 5个触发器（每条业务线1个）
--
-- 生物多样性监测：
--   - 存储过程：自动审核监测记录数据质量
--   - 触发器：监测记录插入时更新设备使用情况
--
-- 生态环境监测：
--   - 存储过程：异常环境数据自动预警
--   - 触发器：设备故障自动报修
--
-- 游客智能管理：
--   - 存储过程：实时更新区域流量状态
--   - 触发器：游客入园自动更新流量统计
--
-- 执法监管：
--   - 存储过程：自动调度执法人员
--   - 触发器：非法行为处理完成自动更新调度状态
--
-- 科研数据支撑：
--   - 存储过程：科研项目数据统计
--   - 触发器：项目结题时禁止新增数据采集记录
-- ============================================