-- 删除并重建数据库，统一使用MySQL 8.0默认字符集
-- DROP DATABASE IF EXISTS national_park_system;

CREATE DATABASE national_park_system 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_0900_ai_ci;  -- 改为MySQL 8.0默认字符集

USE national_park_system;

-- 功能分区表
DROP TABLE IF EXISTS functional_area;
CREATE TABLE functional_area (
    area_id VARCHAR(20) PRIMARY KEY COMMENT '区域编号',
    area_name VARCHAR(100) NOT NULL COMMENT '区域名称',
    area_type VARCHAR(20) NOT NULL CHECK (area_type IN ('核心保护区', '缓冲区', '实验区')) COMMENT '区域类型',
    area_size DECIMAL(10,2) NOT NULL CHECK (area_size > 0) COMMENT '区域面积(公顷)',
    boundary_description TEXT COMMENT '区域边界描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='功能分区表';  -- 改这里
CREATE INDEX idx_area_type ON functional_area(area_type);

-- 用户表
DROP TABLE IF EXISTS system_user;
CREATE TABLE system_user (
    user_id VARCHAR(20) PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户登录名',
    password_hash VARCHAR(128) NOT NULL COMMENT '密码哈希值',
    real_name VARCHAR(50) NOT NULL COMMENT '真实姓名',
    contact_phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    role_type VARCHAR(20) NOT NULL CHECK (role_type IN ('生态监测员', '数据分析师', '游客', '执法人员', '科研人员', '技术人员', '公园管理人员', '系统管理员')) COMMENT '角色类型',
    account_status VARCHAR(10) NOT NULL CHECK (account_status IN ('正常', '锁定', '停用')) COMMENT '账号状态',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    last_login_time DATETIME COMMENT '最后登录时间',
    failed_login_count INT DEFAULT 0 COMMENT '登录失败次数',
    last_failed_login_time DATETIME COMMENT '最后一次登录失败时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
CREATE INDEX idx_user_role ON system_user(role_type);
CREATE INDEX idx_user_status ON system_user(account_status);

DROP TABLE IF EXISTS user_session;
CREATE TABLE user_session (
    session_id VARCHAR(64) PRIMARY KEY COMMENT '会话ID',
    user_id VARCHAR(20) NOT NULL COMMENT '用户ID',
    login_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    last_activity_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后活动时间',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    session_status VARCHAR(10) NOT NULL DEFAULT '有效' CHECK(session_status IN ('有效', '已过期', '已退出')) COMMENT '会话状态',
    FOREIGN KEY (user_id) REFERENCES system_user(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_last_activity (last_activity_time),
    INDEX idx_session_status (session_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户会话表';

-- 物种表
DROP TABLE IF EXISTS species;
CREATE TABLE species (
    species_id VARCHAR(20) PRIMARY KEY COMMENT '物种编号',
    chinese_name VARCHAR(100) NOT NULL COMMENT '物种中文名',
    latin_name VARCHAR(100) NOT NULL COMMENT '物种拉丁名',
    kingdom VARCHAR(50) NOT NULL COMMENT '界',
    phylum VARCHAR(50) NOT NULL COMMENT '门',
    class VARCHAR(50) NOT NULL COMMENT '纲',
    order_name VARCHAR(50) NOT NULL COMMENT '目',
    family VARCHAR(50) NOT NULL COMMENT '科',
    genus VARCHAR(50) NOT NULL COMMENT '属',
    species_name VARCHAR(50) NOT NULL COMMENT '种',
    protection_level VARCHAR(20) NOT NULL CHECK (protection_level IN ('国家一级', '国家二级', '无')) COMMENT '保护级别',
    habitat_description TEXT COMMENT '生存习性',
    distribution_range TEXT COMMENT '分布范围'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='物种表';  -- 改这里
CREATE INDEX idx_species_protection ON species(protection_level);
CREATE INDEX idx_species_chinese_name ON species(chinese_name);

-- 栖息地表
DROP TABLE IF EXISTS habitat;
CREATE TABLE habitat (
    habitat_id VARCHAR(20) PRIMARY KEY COMMENT '栖息地编号',
    area_name VARCHAR(100) NOT NULL COMMENT '区域名称',
    ecology_type VARCHAR(20) NOT NULL CHECK (ecology_type IN ('森林', '湿地', '草原', '其他')) COMMENT '生态类型',
    area_size DECIMAL(10,2) NOT NULL CHECK (area_size > 0) COMMENT '面积(公顷)',
    core_protection_range TEXT COMMENT '核心保护范围',
    suitability_score DECIMAL(3,1) CHECK (suitability_score BETWEEN 0 AND 10) COMMENT '环境适宜性评分'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='栖息地表';  -- 改这里
CREATE INDEX idx_habitat_ecology ON habitat(ecology_type);

-- 监测设备表
DROP TABLE IF EXISTS monitoring_device;
CREATE TABLE monitoring_device (
    device_id VARCHAR(20) PRIMARY KEY COMMENT '设备编号',
    device_type VARCHAR(50) NOT NULL COMMENT '设备类型',
    deployment_area_id VARCHAR(20) NOT NULL COMMENT '部署区域编号',
    installation_date DATE NOT NULL COMMENT '安装日期',
    calibration_cycle INT NOT NULL COMMENT '校准周期(天)',
    operation_status VARCHAR(10) NOT NULL CHECK (operation_status IN ('正常', '故障', '离线')) COMMENT '运行状态',
    communication_protocol VARCHAR(50) NOT NULL COMMENT '通信协议',
    last_calibration_date DATE COMMENT '最后校准日期',
    CONSTRAINT fk_device_area FOREIGN KEY (deployment_area_id) REFERENCES functional_area(area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='监测设备表';  -- 改这里
CREATE INDEX idx_device_area ON monitoring_device(deployment_area_id);
CREATE INDEX idx_device_status ON monitoring_device(operation_status);

-- 监测记录表
DROP TABLE IF EXISTS monitoring_record;
CREATE TABLE monitoring_record (
    record_id VARCHAR(30) PRIMARY KEY COMMENT '记录编号',
    species_id VARCHAR(20) NOT NULL COMMENT '物种编号',
    device_id VARCHAR(20) NOT NULL COMMENT '监测设备编号',
    monitoring_time DATETIME NOT NULL COMMENT '监测时间',
    location_longitude DECIMAL(10,6) NOT NULL COMMENT '位置经度',
    location_latitude DECIMAL(10,6) NOT NULL COMMENT '位置纬度',
    monitoring_method VARCHAR(20) NOT NULL CHECK (monitoring_method IN ('红外相机', '人工巡查', '无人机')) COMMENT '监测方式',
    image_path VARCHAR(255) COMMENT '影像路径',
    quantity INT COMMENT '数量统计',
    behavior_description TEXT COMMENT '行为描述',
    recorder_id VARCHAR(20) NOT NULL COMMENT '记录人ID',
    data_status VARCHAR(10) NOT NULL CHECK (data_status IN ('有效', '待核实')) COMMENT '数据状态',
    CONSTRAINT fk_record_species FOREIGN KEY (species_id) REFERENCES species(species_id),
    CONSTRAINT fk_record_device FOREIGN KEY (device_id) REFERENCES monitoring_device(device_id),
    CONSTRAINT fk_record_user FOREIGN KEY (recorder_id) REFERENCES system_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='监测记录表';  -- 改这里
CREATE INDEX idx_monitoring_species ON monitoring_record(species_id);
CREATE INDEX idx_monitoring_time ON monitoring_record(monitoring_time);
CREATE INDEX idx_monitoring_recorder ON monitoring_record(recorder_id);
CREATE INDEX idx_monitoring_status ON monitoring_record(data_status);

-- 栖息地物种关联表
DROP TABLE IF EXISTS habitat_species;
CREATE TABLE habitat_species (
    habitat_id VARCHAR(20) COMMENT '栖息地编号',
    species_id VARCHAR(20) COMMENT '物种编号',
    is_major_species CHAR(1) NOT NULL CHECK (is_major_species IN ('Y', 'N')) COMMENT '是否主要物种',
    PRIMARY KEY (habitat_id, species_id),
    CONSTRAINT fk_hs_habitat FOREIGN KEY (habitat_id) REFERENCES habitat(habitat_id),
    CONSTRAINT fk_hs_species FOREIGN KEY (species_id) REFERENCES species(species_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='栖息地物种关联表';  -- 改这里

-- 监测指标表
DROP TABLE IF EXISTS monitoring_indicator;
CREATE TABLE monitoring_indicator (
    indicator_id VARCHAR(20) PRIMARY KEY COMMENT '指标编号',
    indicator_name VARCHAR(50) NOT NULL COMMENT '指标名称',
    unit VARCHAR(20) NOT NULL COMMENT '计量单位',
    threshold_upper DECIMAL(10,2) COMMENT '标准阈值上限',
    threshold_lower DECIMAL(10,2) COMMENT '标准阈值下限',
    monitoring_frequency VARCHAR(10) NOT NULL CHECK (monitoring_frequency IN ('小时', '日', '周')) COMMENT '监测频率'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='监测指标表';  -- 改这里
CREATE INDEX idx_indicator_name ON monitoring_indicator(indicator_name);

-- 环境监测数据表
DROP TABLE IF EXISTS environmental_data;
CREATE TABLE environmental_data (
    data_id VARCHAR(30) PRIMARY KEY COMMENT '数据编号',
    indicator_id VARCHAR(20) NOT NULL COMMENT '指标编号',
    device_id VARCHAR(20) NOT NULL COMMENT '设备编号',
    collection_time DATETIME NOT NULL COMMENT '采集时间',
    monitoring_value DECIMAL(10,2) NOT NULL COMMENT '监测值',
    area_id VARCHAR(20) NOT NULL COMMENT '区域编号',
    data_quality VARCHAR(10) NOT NULL CHECK (data_quality IN ('优', '良', '中', '差')) COMMENT '数据质量',
    CONSTRAINT fk_envdata_indicator FOREIGN KEY (indicator_id) REFERENCES monitoring_indicator(indicator_id),
    CONSTRAINT fk_envdata_device FOREIGN KEY (device_id) REFERENCES monitoring_device(device_id),
    CONSTRAINT fk_envdata_area FOREIGN KEY (area_id) REFERENCES functional_area(area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='环境监测数据表';  -- 改这里
CREATE INDEX idx_envdata_indicator ON environmental_data(indicator_id);
CREATE INDEX idx_envdata_time ON environmental_data(collection_time);
CREATE INDEX idx_envdata_area_time ON environmental_data(area_id, collection_time);
CREATE INDEX idx_envdata_quality ON environmental_data(data_quality);

-- 游客表
DROP TABLE IF EXISTS visitor;
CREATE TABLE visitor (
    visitor_id VARCHAR(20) PRIMARY KEY COMMENT '游客ID',
    visitor_name VARCHAR(50) NOT NULL COMMENT '游客姓名',
    id_card_number CHAR(18) NOT NULL UNIQUE COMMENT '身份证号',
    contact_phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    entry_time DATETIME COMMENT '入园时间',
    exit_time DATETIME COMMENT '离园时间',
    entry_method VARCHAR(20) NOT NULL CHECK (entry_method IN ('线上预约', '现场购票')) COMMENT '入园方式',
    CONSTRAINT chk_visitor_time CHECK (exit_time IS NULL OR exit_time >= entry_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='游客表';  -- 改这里
CREATE INDEX idx_visitor_idcard ON visitor(id_card_number);
CREATE INDEX idx_visitor_entry_time ON visitor(entry_time);

-- 预约记录表
DROP TABLE IF EXISTS reservation;
CREATE TABLE reservation (
    reservation_id VARCHAR(30) PRIMARY KEY COMMENT '预约编号',
    visitor_id VARCHAR(20) NOT NULL COMMENT '游客ID',
    reservation_date DATE NOT NULL COMMENT '预约日期',
    entry_time_slot VARCHAR(20) NOT NULL COMMENT '入园时段',
    party_size INT NOT NULL CHECK (party_size > 0) COMMENT '同行人数',
    reservation_status VARCHAR(10) NOT NULL CHECK (reservation_status IN ('已确认', '已取消', '已完成')) COMMENT '预约状态',
    ticket_amount DECIMAL(10,2) NOT NULL CHECK (ticket_amount >= 0) COMMENT '购票金额',
    payment_status VARCHAR(10) NOT NULL CHECK (payment_status IN ('已支付', '未支付')) COMMENT '支付状态',
    CONSTRAINT fk_reservation_visitor FOREIGN KEY (visitor_id) REFERENCES visitor(visitor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='预约记录表';  -- 改这里
CREATE INDEX idx_reservation_visitor ON reservation(visitor_id);
CREATE INDEX idx_reservation_date ON reservation(reservation_date);
CREATE INDEX idx_reservation_status ON reservation(reservation_status);

-- 游客轨迹表
DROP TABLE IF EXISTS visitor_trajectory;
CREATE TABLE visitor_trajectory (
    trajectory_id VARCHAR(30) PRIMARY KEY COMMENT '轨迹编号',
    visitor_id VARCHAR(20) NOT NULL COMMENT '游客ID',
    tracking_time DATETIME NOT NULL COMMENT '定位时间',
    location_longitude DECIMAL(10,6) NOT NULL COMMENT '位置经度',
    location_latitude DECIMAL(10,6) NOT NULL COMMENT '位置纬度',
    area_id VARCHAR(20) NOT NULL COMMENT '所在区域编号',
    out_of_route CHAR(1) NOT NULL CHECK (out_of_route IN ('Y', 'N')) COMMENT '是否超出路线',
    CONSTRAINT fk_trajectory_visitor FOREIGN KEY (visitor_id) REFERENCES visitor(visitor_id),
    CONSTRAINT fk_trajectory_area FOREIGN KEY (area_id) REFERENCES functional_area(area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='游客轨迹表';  -- 改这里
CREATE INDEX idx_trajectory_visitor_time ON visitor_trajectory(visitor_id, tracking_time);
CREATE INDEX idx_trajectory_area ON visitor_trajectory(area_id);
CREATE INDEX idx_trajectory_out_of_route ON visitor_trajectory(out_of_route);

-- 流量控制表
DROP TABLE IF EXISTS traffic_control;
CREATE TABLE traffic_control (
    area_id VARCHAR(20) PRIMARY KEY COMMENT '区域编号',
    daily_capacity INT NOT NULL CHECK (daily_capacity > 0) COMMENT '日最大承载量',
    current_visitor_count INT NOT NULL DEFAULT 0 CHECK (current_visitor_count >= 0) COMMENT '当前在园人数',
    warning_threshold INT NOT NULL CHECK (warning_threshold > 0) COMMENT '预警阈值',
    current_status VARCHAR(10) NOT NULL CHECK (current_status IN ('正常', '预警', '限流')) COMMENT '当前状态',
    CONSTRAINT fk_traffic_area FOREIGN KEY (area_id) REFERENCES functional_area(area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='流量控制表';  -- 改这里
CREATE INDEX idx_traffic_status ON traffic_control(current_status);

-- 执法人员表
DROP TABLE IF EXISTS law_enforcer;
CREATE TABLE law_enforcer (
    enforcer_id VARCHAR(20) PRIMARY KEY COMMENT '执法ID',
    enforcer_name VARCHAR(50) NOT NULL COMMENT '执法人员姓名',
    department VARCHAR(50) NOT NULL COMMENT '所属部门',
    enforcement_authority VARCHAR(50) NOT NULL COMMENT '执法权限',
    contact_phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    equipment_id VARCHAR(20) COMMENT '执法设备编号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='执法人员表';  -- 改这里
CREATE INDEX idx_enforcer_department ON law_enforcer(department);

-- 视频监控点表
DROP TABLE IF EXISTS surveillance_point;
CREATE TABLE surveillance_point (
    monitor_id VARCHAR(20) PRIMARY KEY COMMENT '监控点编号',
    area_id VARCHAR(20) NOT NULL COMMENT '部署区域编号',
    location_longitude DECIMAL(10,6) NOT NULL COMMENT '位置经度',
    location_latitude DECIMAL(10,6) NOT NULL COMMENT '位置纬度',
    monitoring_range TEXT COMMENT '监控范围',
    device_status VARCHAR(10) NOT NULL CHECK (device_status IN ('正常', '故障')) COMMENT '设备状态',
    storage_period INT NOT NULL DEFAULT 90 CHECK (storage_period > 0) COMMENT '存储周期(天)',
    CONSTRAINT fk_surveillance_area FOREIGN KEY (area_id) REFERENCES functional_area(area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='视频监控点表';  -- 改这里
CREATE INDEX idx_surveillance_area ON surveillance_point(area_id);
CREATE INDEX idx_surveillance_status ON surveillance_point(device_status);

-- 非法行为记录表
DROP TABLE IF EXISTS illegal_behavior;
CREATE TABLE illegal_behavior (
    record_id VARCHAR(30) PRIMARY KEY COMMENT '记录编号',
    behavior_type VARCHAR(50) NOT NULL COMMENT '行为类型',
    occurrence_time DATETIME NOT NULL COMMENT '发生时间',
    area_id VARCHAR(20) NOT NULL COMMENT '发生区域编号',
    evidence_path VARCHAR(255) NOT NULL COMMENT '证据路径',
    handling_status VARCHAR(10) NOT NULL CHECK (handling_status IN ('未处理', '处理中', '已结案')) COMMENT '处理状态',
    enforcer_id VARCHAR(20) COMMENT '执法ID',
    handling_result TEXT COMMENT '处理结果',
    penalty_basis TEXT COMMENT '处罚依据',
    CONSTRAINT fk_illegal_area FOREIGN KEY (area_id) REFERENCES functional_area(area_id),
    CONSTRAINT fk_illegal_enforcer FOREIGN KEY (enforcer_id) REFERENCES law_enforcer(enforcer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='非法行为记录表';  -- 改这里
CREATE INDEX idx_illegal_time ON illegal_behavior(occurrence_time);
CREATE INDEX idx_illegal_status ON illegal_behavior(handling_status);
CREATE INDEX idx_illegal_enforcer ON illegal_behavior(enforcer_id);
CREATE INDEX idx_illegal_area ON illegal_behavior(area_id);

-- 执法调度表
DROP TABLE IF EXISTS enforcement_dispatch;
CREATE TABLE enforcement_dispatch (
    dispatch_id VARCHAR(30) PRIMARY KEY COMMENT '调度编号',
    record_id VARCHAR(30) NOT NULL COMMENT '非法行为记录编号',
    enforcer_id VARCHAR(20) NOT NULL COMMENT '执法ID',
    dispatch_time DATETIME NOT NULL COMMENT '调度时间',
    response_time DATETIME COMMENT '响应时间',
    completion_time DATETIME COMMENT '完成时间',
    dispatch_status VARCHAR(10) NOT NULL CHECK (dispatch_status IN ('待响应', '已派单', '已完成')) COMMENT '调度状态',
    CONSTRAINT chk_dispatch_response CHECK (response_time IS NULL OR response_time >= dispatch_time),
    CONSTRAINT chk_dispatch_completion CHECK (completion_time IS NULL OR completion_time >= response_time),
    CONSTRAINT fk_dispatch_record FOREIGN KEY (record_id) REFERENCES illegal_behavior(record_id),
    CONSTRAINT fk_dispatch_enforcer FOREIGN KEY (enforcer_id) REFERENCES law_enforcer(enforcer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='执法调度表';  -- 改这里
CREATE INDEX idx_dispatch_record ON enforcement_dispatch(record_id);
CREATE INDEX idx_dispatch_enforcer ON enforcement_dispatch(enforcer_id);
CREATE INDEX idx_dispatch_status ON enforcement_dispatch(dispatch_status);
CREATE INDEX idx_dispatch_time ON enforcement_dispatch(dispatch_time);

-- 科研项目表
DROP TABLE IF EXISTS research_project;
CREATE TABLE research_project (
    project_id VARCHAR(20) PRIMARY KEY COMMENT '项目编号',
    project_name VARCHAR(100) NOT NULL COMMENT '项目名称',
    principal_id VARCHAR(20) NOT NULL COMMENT '负责人ID',
    applicant_unit VARCHAR(100) NOT NULL COMMENT '申请单位',
    start_date DATE NOT NULL COMMENT '立项日期',
    end_date DATE COMMENT '结题日期',
    project_status VARCHAR(10) NOT NULL CHECK (project_status IN ('在研', '已结题', '暂停')) COMMENT '项目状态',
    research_field VARCHAR(50) NOT NULL COMMENT '研究领域',
    CONSTRAINT chk_project_date CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT fk_project_principal FOREIGN KEY (principal_id) REFERENCES system_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='科研项目表';  -- 改这里
CREATE INDEX idx_project_principal ON research_project(principal_id);
CREATE INDEX idx_project_status ON research_project(project_status);
CREATE INDEX idx_project_field ON research_project(research_field);

-- 科研数据采集记录表
DROP TABLE IF EXISTS research_data_collection;
CREATE TABLE research_data_collection (
    collection_id VARCHAR(30) PRIMARY KEY COMMENT '采集编号',
    project_id VARCHAR(20) NOT NULL COMMENT '项目编号',
    collector_id VARCHAR(20) NOT NULL COMMENT '采集人ID',
    collection_time DATETIME NOT NULL COMMENT '采集时间',
    area_id VARCHAR(20) NOT NULL COMMENT '区域编号',
    collection_content TEXT NOT NULL COMMENT '采集内容',
    sample_number VARCHAR(30) COMMENT '样本编号',
    monitoring_data_id VARCHAR(30) COMMENT '监测数据编号',
    survey_record TEXT COMMENT '调查记录',
    data_source VARCHAR(20) NOT NULL CHECK (data_source IN ('实地采集', '系统调用')) COMMENT '数据来源',
    CONSTRAINT fk_collection_project FOREIGN KEY (project_id) REFERENCES research_project(project_id),
    CONSTRAINT fk_collection_collector FOREIGN KEY (collector_id) REFERENCES system_user(user_id),
    CONSTRAINT fk_collection_area FOREIGN KEY (area_id) REFERENCES functional_area(area_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='科研数据采集记录表';  -- 改这里
CREATE INDEX idx_research_project ON research_data_collection(project_id);
CREATE INDEX idx_research_collector ON research_data_collection(collector_id);
CREATE INDEX idx_research_time ON research_data_collection(collection_time);
CREATE INDEX idx_research_area ON research_data_collection(area_id);

-- 科研成果表
DROP TABLE IF EXISTS research_achievement;
CREATE TABLE research_achievement (
    achievement_id VARCHAR(30) PRIMARY KEY COMMENT '成果编号',
    project_id VARCHAR(20) NOT NULL COMMENT '项目编号',
    achievement_type VARCHAR(20) NOT NULL CHECK (achievement_type IN ('论文', '报告', '专利', '其他')) COMMENT '成果类型',
    achievement_name VARCHAR(200) NOT NULL COMMENT '成果名称',
    publish_date DATE NOT NULL COMMENT '发表日期',
    share_permission VARCHAR(10) NOT NULL CHECK (share_permission IN ('公开', '内部共享', '保密')) COMMENT '共享权限',
    file_path VARCHAR(255) COMMENT '文件路径',
    CONSTRAINT fk_achievement_project FOREIGN KEY (project_id) REFERENCES research_project(project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='科研成果表';  -- 改这里
CREATE INDEX idx_achievement_project ON research_achievement(project_id);
CREATE INDEX idx_achievement_type ON research_achievement(achievement_type);
CREATE INDEX idx_achievement_permission ON research_achievement(share_permission);

SET FOREIGN_KEY_CHECKS = 1;