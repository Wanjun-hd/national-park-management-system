from dao.monitoring_dao import MonitoringDAO

# 创建DAO实例
dao = MonitoringDAO()

# 查询国家一级保护物种
species_list = dao.query_species_by_protection_level('国家一级')
print(species_list)

# 插入监测记录
record_data = {
    'record_id': 'MR2024120999',
    'species_id': 'SP001',
    'device_id': 'DEV001',
    # ... 其他字段
}
result = dao.insert_monitoring_record(record_data)
print(f"插入成功，影响{result}行")