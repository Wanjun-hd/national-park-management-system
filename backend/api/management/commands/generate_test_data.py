from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from api.models import *
import random


class Command(BaseCommand):
    help = '生成测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始生成测试数据...')

        # 生成物种数据
        self.generate_species()

        # 生成栖息地数据
        self.generate_habitats()

        # 生成监测设备
        self.generate_devices()

        # 生成监测记录
        self.generate_monitoring_records()

        # 生成环境指标
        self.generate_indicators()

        # 生成环境数据
        self.generate_environment_data()

        # 生成游客数据
        self.generate_visitors()

        # 生成预约数据
        self.generate_reservations()

        # 生成违法行为数据
        self.generate_illegal_behaviors()

        # 生成科研项目
        self.generate_research_projects()

        self.stdout.write(self.style.SUCCESS('测试数据生成完成！'))

    def generate_species(self):
        species_data = [
            ('S001', '大熊猫', 'Ailuropoda melanoleuca', '动物界', '脊索动物门', '哺乳纲', '食肉目', '熊科', 'Ailuropoda', 'melanoleuca', '国家一级'),
            ('S002', '金丝猴', 'Rhinopithecus roxellana', '动物界', '脊索动物门', '哺乳纲', '灵长目', '猴科', 'Rhinopithecus', 'roxellana', '国家一级'),
            ('S003', '朱鹮', 'Nipponia nippon', '动物界', '脊索动物门', '鸟纲', '鹳形目', '朱鹮科', 'Nipponia', 'nippon', '国家一级'),
            ('S004', '东北虎', 'Panthera tigris altaica', '动物界', '脊索动物门', '哺乳纲', '食肉目', '猫科', 'Panthera', 'tigris', '国家一级'),
            ('S005', '雪豹', 'Panthera uncia', '动物界', '脊索动物门', '哺乳纲', '食肉目', '猫科', 'Panthera', 'uncia', '国家一级'),
        ]

        for data in species_data:
            Species.objects.get_or_create(
                species_id=data[0],
                defaults={
                    'chinese_name': data[1],
                    'latin_name': data[2],
                    'kingdom': data[3],
                    'phylum': data[4],
                    'class_field': data[5],
                    'order_name': data[6],
                    'family': data[7],
                    'genus': data[8],
                    'species_name': data[9],
                    'protection_level': data[10]
                }
            )
        self.stdout.write('物种数据生成完成')

    def generate_habitats(self):
        habitats_data = [
            ('H001', 'A001', '核心保护区1号', '森林', 1500.0, 103.5, 31.2),
            ('H002', 'A002', '缓冲区2号', '竹林', 800.0, 103.6, 31.3),
        ]

        for data in habitats_data:
            Habitat.objects.get_or_create(
                habitat_id=data[0],
                defaults={
                    'area_id': data[1],
                    'habitat_name': data[2],
                    'ecology_type': data[3],
                    'area_size': data[4],
                    'longitude': data[5],
                    'latitude': data[6]
                }
            )
        self.stdout.write('栖息地数据生成完成')

    def generate_devices(self):
        devices_data = [
            ('D001', 'H001', '红外相机01', '红外相机', '正常', '2024-01-01'),
            ('D002', 'H001', '红外相机02', '红外相机', '正常', '2024-01-01'),
            ('D003', 'H002', '红外相机03', '红外相机', '正常', '2024-01-01'),
        ]

        for data in devices_data:
            MonitoringDevice.objects.get_or_create(
                device_id=data[0],
                defaults={
                    'location': data[1],
                    'device_name': data[2],
                    'device_type': data[3],
                    'operation_status': data[4],
                    'installation_date': data[5]
                }
            )
        self.stdout.write('监测设备数据生成完成')

    def generate_monitoring_records(self):
        species = list(Species.objects.all())
        devices = list(MonitoringDevice.objects.all())

        if not species or not devices:
            return

        for i in range(30):
            date = datetime.now() - timedelta(days=random.randint(0, 90))
            MonitoringRecord.objects.get_or_create(
                record_id=f'MR{str(i+1).zfill(3)}',
                defaults={
                    'species': random.choice(species),
                    'device': random.choice(devices),
                    'monitoring_time': date,
                    'monitoring_method': '红外相机',
                    'quantity': random.randint(1, 5),
                    'behavior_description': '正常活动',
                    'data_status': '有效',
                    'recorder_id': 'U002'
                }
            )
        self.stdout.write('监测记录数据生成完成')

    def generate_indicators(self):
        indicators_data = [
            ('IND001', '温度', '摄氏度', -10.0, 40.0),
            ('IND002', '湿度', '百分比', 0.0, 100.0),
            ('IND003', '空气质量', 'AQI', 0.0, 500.0),
        ]

        for data in indicators_data:
            EnvironmentIndicator.objects.get_or_create(
                indicator_id=data[0],
                defaults={
                    'indicator_name': data[1],
                    'unit': data[2],
                    'min_normal_value': data[3],
                    'max_normal_value': data[4]
                }
            )
        self.stdout.write('环境指标数据生成完成')

    def generate_environment_data(self):
        indicators = list(EnvironmentIndicator.objects.all())
        devices = list(MonitoringDevice.objects.all())

        if not indicators or not devices:
            return

        for i in range(50):
            date = datetime.now() - timedelta(hours=random.randint(0, 720))
            EnvironmentData.objects.get_or_create(
                data_id=f'ED{str(i+1).zfill(4)}',
                defaults={
                    'indicator': random.choice(indicators),
                    'device': random.choice(devices),
                    'area_id': 'A001',
                    'collection_time': date,
                    'monitoring_value': round(random.uniform(15.0, 30.0), 2),
                    'data_quality': random.choice(['优秀', '良好', '一般'])
                }
            )
        self.stdout.write('环境数据生成完成')

    def generate_visitors(self):
        for i in range(25):
            date = datetime.now() - timedelta(days=random.randint(0, 30))
            Visitor.objects.get_or_create(
                visitor_id=f'V{str(i+1).zfill(3)}',
                defaults={
                    'name': f'游客{i+1}',
                    'id_card': f'11010119900101{str(1000+i)}',
                    'phone': f'138{str(10000000+i)}',
                    'entry_time': date,
                    'exit_time': date + timedelta(hours=random.randint(2, 8)) if random.random() > 0.3 else None
                }
            )
        self.stdout.write('游客数据生成完成')

    def generate_reservations(self):
        visitors = list(Visitor.objects.all()[:10])

        if not visitors:
            return

        for i, visitor in enumerate(visitors):
            date = datetime.now() + timedelta(days=random.randint(1, 30))
            Reservation.objects.get_or_create(
                reservation_id=f'R{str(i+1).zfill(4)}',
                defaults={
                    'visitor': visitor,
                    'reservation_date': date.date(),
                    'visitor_count': random.randint(1, 4),
                    'contact_phone': visitor.phone,
                    'total_amount': random.randint(100, 500),
                    'payment_status': random.choice(['已支付', '未支付']),
                    'reservation_status': random.choice(['已确认', '待确认'])
                }
            )
        self.stdout.write('预约数据生成完成')

    def generate_illegal_behaviors(self):
        for i in range(10):
            date = datetime.now() - timedelta(days=random.randint(0, 60))
            IllegalBehavior.objects.get_or_create(
                behavior_id=f'IB{str(i+1).zfill(3)}',
                defaults={
                    'occurrence_time': date,
                    'area_id': 'A001',
                    'behavior_type': random.choice(['非法狩猎', '乱扔垃圾', '破坏植被']),
                    'severity_level': random.choice(['轻微', '一般', '严重']),
                    'handling_status': random.choice(['未处理', '处理中', '已处理']),
                    'reporter_id': 'U002'
                }
            )
        self.stdout.write('违法行为数据生成完成')

    def generate_research_projects(self):
        projects_data = [
            ('P001', '大熊猫栖息地研究', '生态学', '在研', '2024-01-01', None),
            ('P002', '生物多样性调查', '生物学', '在研', '2024-02-01', None),
        ]

        for data in projects_data:
            ResearchProject.objects.get_or_create(
                project_id=data[0],
                defaults={
                    'project_name': data[1],
                    'research_field': data[2],
                    'project_status': data[3],
                    'start_date': data[4],
                    'end_date': data[5],
                    'leader_id': 'U002'
                }
            )
        self.stdout.write('科研项目数据生成完成')
