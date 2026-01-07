"""
Django Models for National Park Management System
Based on existing database schema with 21 tables
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class FunctionalArea(models.Model):
    """功能分区表"""
    AREA_TYPE_CHOICES = [
        ('核心保护区', '核心保护区'),
        ('缓冲区', '缓冲区'),
        ('实验区', '实验区'),
    ]

    area_id = models.CharField(max_length=20, primary_key=True, verbose_name='区域编号')
    area_name = models.CharField(max_length=100, verbose_name='区域名称')
    area_type = models.CharField(max_length=20, choices=AREA_TYPE_CHOICES, verbose_name='区域类型')
    area_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='区域面积(公顷)'
    )
    boundary_description = models.TextField(blank=True, null=True, verbose_name='区域边界描述')

    class Meta:
        db_table = 'functional_area'
        managed = False
        verbose_name = '功能分区'
        verbose_name_plural = '功能分区'
        indexes = [
            models.Index(fields=['area_type'], name='idx_area_type'),
        ]

    def __str__(self):
        return f"{self.area_name} ({self.area_type})"


class SystemUser(models.Model):
    """用户表"""
    ROLE_CHOICES = [
        ('生态监测员', '生态监测员'),
        ('数据分析师', '数据分析师'),
        ('游客', '游客'),
        ('执法人员', '执法人员'),
        ('科研人员', '科研人员'),
        ('技术人员', '技术人员'),
        ('公园管理人员', '公园管理人员'),
        ('系统管理员', '系统管理员'),
    ]

    STATUS_CHOICES = [
        ('正常', '正常'),
        ('锁定', '锁定'),
        ('停用', '停用'),
    ]

    user_id = models.CharField(max_length=20, primary_key=True, verbose_name='用户ID')
    username = models.CharField(max_length=50, unique=True, verbose_name='用户登录名')
    password_hash = models.CharField(max_length=128, verbose_name='密码哈希值')
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色类型')
    account_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='账号状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_login_time = models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')
    failed_login_count = models.IntegerField(default=0, verbose_name='登录失败次数')
    last_failed_login_time = models.DateTimeField(blank=True, null=True, verbose_name='最后一次登录失败时间')

    class Meta:
        db_table = 'system_user'
        managed = False
        verbose_name = '系统用户'
        verbose_name_plural = '系统用户'
        indexes = [
            models.Index(fields=['role_type'], name='idx_user_role'),
            models.Index(fields=['account_status'], name='idx_user_status'),
        ]

    def __str__(self):
        return f"{self.real_name} ({self.username})"


class UserSession(models.Model):
    """用户会话表"""
    STATUS_CHOICES = [
        ('有效', '有效'),
        ('已过期', '已过期'),
        ('已退出', '已退出'),
    ]

    session_id = models.CharField(max_length=64, primary_key=True, verbose_name='会话ID')
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, db_column='user_id', verbose_name='用户')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    last_activity_time = models.DateTimeField(auto_now=True, verbose_name='最后活动时间')
    ip_address = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP地址')
    session_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='有效', verbose_name='会话状态')

    class Meta:
        db_table = 'user_session'
        managed = False
        verbose_name = '用户会话'
        verbose_name_plural = '用户会话'
        indexes = [
            models.Index(fields=['user'], name='idx_user_id'),
            models.Index(fields=['last_activity_time'], name='idx_last_activity'),
            models.Index(fields=['session_status'], name='idx_session_status'),
        ]

    def __str__(self):
        return f"Session {self.session_id[:8]}... - {self.user.username}"


class Species(models.Model):
    """物种表"""
    PROTECTION_CHOICES = [
        ('国家一级', '国家一级'),
        ('国家二级', '国家二级'),
        ('无', '无'),
    ]

    species_id = models.CharField(max_length=20, primary_key=True, verbose_name='物种编号')
    chinese_name = models.CharField(max_length=100, verbose_name='物种中文名')
    latin_name = models.CharField(max_length=100, verbose_name='物种拉丁名')
    kingdom = models.CharField(max_length=50, verbose_name='界')
    phylum = models.CharField(max_length=50, verbose_name='门')
    class_field = models.CharField(max_length=50, db_column='class', verbose_name='纲')
    order_name = models.CharField(max_length=50, verbose_name='目')
    family = models.CharField(max_length=50, verbose_name='科')
    genus = models.CharField(max_length=50, verbose_name='属')
    species_name = models.CharField(max_length=50, verbose_name='种')
    protection_level = models.CharField(max_length=20, choices=PROTECTION_CHOICES, verbose_name='保护级别')
    habitat_description = models.TextField(blank=True, null=True, verbose_name='生存习性')
    distribution_range = models.TextField(blank=True, null=True, verbose_name='分布范围')

    class Meta:
        db_table = 'species'
        managed = False
        verbose_name = '物种'
        verbose_name_plural = '物种'
        indexes = [
            models.Index(fields=['protection_level'], name='idx_species_protection'),
            models.Index(fields=['chinese_name'], name='idx_species_chinese_name'),
        ]

    def __str__(self):
        return f"{self.chinese_name} ({self.latin_name})"


class Habitat(models.Model):
    """栖息地表"""
    ECOLOGY_CHOICES = [
        ('森林', '森林'),
        ('湿地', '湿地'),
        ('草原', '草原'),
        ('其他', '其他'),
    ]

    habitat_id = models.CharField(max_length=20, primary_key=True, verbose_name='栖息地编号')
    area_name = models.CharField(max_length=100, verbose_name='区域名称')
    ecology_type = models.CharField(max_length=20, choices=ECOLOGY_CHOICES, verbose_name='生态类型')
    area_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='面积(公顷)'
    )
    core_protection_range = models.TextField(blank=True, null=True, verbose_name='核心保护范围')
    suitability_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('10'))],
        verbose_name='环境适宜性评分'
    )

    class Meta:
        db_table = 'habitat'
        managed = False
        verbose_name = '栖息地'
        verbose_name_plural = '栖息地'
        indexes = [
            models.Index(fields=['ecology_type'], name='idx_habitat_ecology'),
        ]

    def __str__(self):
        return f"{self.area_name} ({self.ecology_type})"


class MonitoringDevice(models.Model):
    """监测设备表"""
    STATUS_CHOICES = [
        ('正常', '正常'),
        ('故障', '故障'),
        ('离线', '离线'),
    ]

    device_id = models.CharField(max_length=20, primary_key=True, verbose_name='设备编号')
    device_type = models.CharField(max_length=50, verbose_name='设备类型')
    deployment_area = models.ForeignKey(
        FunctionalArea,
        on_delete=models.CASCADE,
        db_column='deployment_area_id',
        verbose_name='部署区域'
    )
    installation_date = models.DateField(verbose_name='安装日期')
    calibration_cycle = models.IntegerField(verbose_name='校准周期(天)')
    operation_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='运行状态')
    communication_protocol = models.CharField(max_length=50, verbose_name='通信协议')
    last_calibration_date = models.DateField(blank=True, null=True, verbose_name='最后校准日期')

    class Meta:
        db_table = 'monitoring_device'
        managed = False
        verbose_name = '监测设备'
        verbose_name_plural = '监测设备'
        indexes = [
            models.Index(fields=['deployment_area'], name='idx_device_area'),
            models.Index(fields=['operation_status'], name='idx_device_status'),
        ]

    def __str__(self):
        return f"{self.device_type} ({self.device_id})"


class MonitoringRecord(models.Model):
    """监测记录表"""
    METHOD_CHOICES = [
        ('红外相机', '红外相机'),
        ('人工巡查', '人工巡查'),
        ('无人机', '无人机'),
    ]

    STATUS_CHOICES = [
        ('有效', '有效'),
        ('待核实', '待核实'),
    ]

    record_id = models.CharField(max_length=30, primary_key=True, verbose_name='记录编号')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, db_column='species_id', verbose_name='物种')
    device = models.ForeignKey(MonitoringDevice, on_delete=models.CASCADE, db_column='device_id', verbose_name='监测设备')
    monitoring_time = models.DateTimeField(verbose_name='监测时间')
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='位置经度')
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='位置纬度')
    monitoring_method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name='监测方式')
    image_path = models.CharField(max_length=255, blank=True, null=True, verbose_name='影像路径')
    quantity = models.IntegerField(blank=True, null=True, verbose_name='数量统计')
    behavior_description = models.TextField(blank=True, null=True, verbose_name='行为描述')
    recorder = models.ForeignKey(SystemUser, on_delete=models.CASCADE, db_column='recorder_id', verbose_name='记录人')
    data_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='数据状态')

    class Meta:
        db_table = 'monitoring_record'
        managed = False
        verbose_name = '监测记录'
        verbose_name_plural = '监测记录'
        indexes = [
            models.Index(fields=['species'], name='idx_monitoring_species'),
            models.Index(fields=['monitoring_time'], name='idx_monitoring_time'),
            models.Index(fields=['recorder'], name='idx_monitoring_recorder'),
            models.Index(fields=['data_status'], name='idx_monitoring_status'),
        ]

    def __str__(self):
        return f"{self.species.chinese_name} - {self.monitoring_time}"


class HabitatSpecies(models.Model):
    """栖息地物种关联表"""
    MAJOR_CHOICES = [
        ('Y', '是'),
        ('N', '否'),
    ]

    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE, db_column='habitat_id', verbose_name='栖息地')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, db_column='species_id', verbose_name='物种')
    is_major_species = models.CharField(max_length=1, choices=MAJOR_CHOICES, verbose_name='是否主要物种')

    class Meta:
        db_table = 'habitat_species'
        managed = False
        unique_together = [['habitat', 'species']]
        verbose_name = '栖息地物种关联'
        verbose_name_plural = '栖息地物种关联'

    def __str__(self):
        return f"{self.habitat.area_name} - {self.species.chinese_name}"


class MonitoringIndicator(models.Model):
    """监测指标表"""
    FREQUENCY_CHOICES = [
        ('小时', '小时'),
        ('日', '日'),
        ('周', '周'),
    ]

    indicator_id = models.CharField(max_length=20, primary_key=True, verbose_name='指标编号')
    indicator_name = models.CharField(max_length=50, verbose_name='指标名称')
    unit = models.CharField(max_length=20, verbose_name='计量单位')
    threshold_upper = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='标准阈值上限'
    )
    threshold_lower = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='标准阈值下限'
    )
    monitoring_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='监测频率')

    class Meta:
        db_table = 'monitoring_indicator'
        managed = False
        verbose_name = '监测指标'
        verbose_name_plural = '监测指标'
        indexes = [
            models.Index(fields=['indicator_name'], name='idx_indicator_name'),
        ]

    def __str__(self):
        return f"{self.indicator_name} ({self.unit})"


class EnvironmentalData(models.Model):
    """环境监测数据表"""
    QUALITY_CHOICES = [
        ('优', '优'),
        ('良', '良'),
        ('中', '中'),
        ('差', '差'),
    ]

    data_id = models.CharField(max_length=30, primary_key=True, verbose_name='数据编号')
    indicator = models.ForeignKey(MonitoringIndicator, on_delete=models.CASCADE, db_column='indicator_id', verbose_name='指标')
    device = models.ForeignKey(MonitoringDevice, on_delete=models.CASCADE, db_column='device_id', verbose_name='设备')
    collection_time = models.DateTimeField(verbose_name='采集时间')
    monitoring_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='监测值')
    area = models.ForeignKey(FunctionalArea, on_delete=models.CASCADE, db_column='area_id', verbose_name='区域')
    data_quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, verbose_name='数据质量')

    class Meta:
        db_table = 'environmental_data'
        managed = False
        verbose_name = '环境监测数据'
        verbose_name_plural = '环境监测数据'
        indexes = [
            models.Index(fields=['indicator'], name='idx_envdata_indicator'),
            models.Index(fields=['collection_time'], name='idx_envdata_time'),
            models.Index(fields=['area', 'collection_time'], name='idx_envdata_area_time'),
            models.Index(fields=['data_quality'], name='idx_envdata_quality'),
        ]

    def __str__(self):
        return f"{self.indicator.indicator_name} - {self.collection_time}"


class Visitor(models.Model):
    """游客表"""
    ENTRY_METHOD_CHOICES = [
        ('线上预约', '线上预约'),
        ('现场购票', '现场购票'),
    ]

    visitor_id = models.CharField(max_length=20, primary_key=True, verbose_name='游客ID')
    visitor_name = models.CharField(max_length=50, verbose_name='游客姓名')
    id_card_number = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    entry_time = models.DateTimeField(blank=True, null=True, verbose_name='入园时间')
    exit_time = models.DateTimeField(blank=True, null=True, verbose_name='离园时间')
    entry_method = models.CharField(max_length=20, choices=ENTRY_METHOD_CHOICES, verbose_name='入园方式')

    class Meta:
        db_table = 'visitor'
        managed = False
        verbose_name = '游客'
        verbose_name_plural = '游客'
        indexes = [
            models.Index(fields=['id_card_number'], name='idx_visitor_idcard'),
            models.Index(fields=['entry_time'], name='idx_visitor_entry_time'),
        ]

    def __str__(self):
        return f"{self.visitor_name} ({self.id_card_number})"


class Reservation(models.Model):
    """预约记录表"""
    STATUS_CHOICES = [
        ('已确认', '已确认'),
        ('已取消', '已取消'),
        ('已完成', '已完成'),
    ]

    PAYMENT_CHOICES = [
        ('已支付', '已支付'),
        ('未支付', '未支付'),
    ]

    reservation_id = models.CharField(max_length=30, primary_key=True, verbose_name='预约编号')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, db_column='visitor_id', verbose_name='游客')
    reservation_date = models.DateField(verbose_name='预约日期')
    entry_time_slot = models.CharField(max_length=20, verbose_name='入园时段')
    party_size = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='同行人数')
    reservation_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='预约状态')
    ticket_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='购票金额'
    )
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name='支付状态')

    class Meta:
        db_table = 'reservation'
        managed = False
        verbose_name = '预约记录'
        verbose_name_plural = '预约记录'
        indexes = [
            models.Index(fields=['visitor'], name='idx_reservation_visitor'),
            models.Index(fields=['reservation_date'], name='idx_reservation_date'),
            models.Index(fields=['reservation_status'], name='idx_reservation_status'),
        ]

    def __str__(self):
        return f"{self.visitor.visitor_name} - {self.reservation_date}"


class VisitorTrajectory(models.Model):
    """游客轨迹表"""
    OUT_OF_ROUTE_CHOICES = [
        ('Y', '是'),
        ('N', '否'),
    ]

    trajectory_id = models.CharField(max_length=30, primary_key=True, verbose_name='轨迹编号')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, db_column='visitor_id', verbose_name='游客')
    tracking_time = models.DateTimeField(verbose_name='定位时间')
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='位置经度')
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='位置纬度')
    area = models.ForeignKey(FunctionalArea, on_delete=models.CASCADE, db_column='area_id', verbose_name='所在区域')
    out_of_route = models.CharField(max_length=1, choices=OUT_OF_ROUTE_CHOICES, verbose_name='是否超出路线')

    class Meta:
        db_table = 'visitor_trajectory'
        managed = False
        verbose_name = '游客轨迹'
        verbose_name_plural = '游客轨迹'
        indexes = [
            models.Index(fields=['visitor', 'tracking_time'], name='idx_trajectory_visitor_time'),
            models.Index(fields=['area'], name='idx_trajectory_area'),
            models.Index(fields=['out_of_route'], name='idx_trajectory_out_of_route'),
        ]

    def __str__(self):
        return f"{self.visitor.visitor_name} - {self.tracking_time}"


class TrafficControl(models.Model):
    """流量控制表"""
    STATUS_CHOICES = [
        ('正常', '正常'),
        ('预警', '预警'),
        ('限流', '限流'),
    ]

    area = models.OneToOneField(
        FunctionalArea,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='area_id',
        verbose_name='区域'
    )
    daily_capacity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='日最大承载量')
    current_visitor_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='当前在园人数'
    )
    warning_threshold = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='预警阈值')
    current_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='当前状态')

    class Meta:
        db_table = 'traffic_control'
        managed = False
        verbose_name = '流量控制'
        verbose_name_plural = '流量控制'
        indexes = [
            models.Index(fields=['current_status'], name='idx_traffic_status'),
        ]

    def __str__(self):
        return f"{self.area.area_name} - {self.current_status}"


class LawEnforcer(models.Model):
    """执法人员表"""
    enforcer_id = models.CharField(max_length=20, primary_key=True, verbose_name='执法ID')
    enforcer_name = models.CharField(max_length=50, verbose_name='执法人员姓名')
    department = models.CharField(max_length=50, verbose_name='所属部门')
    enforcement_authority = models.CharField(max_length=50, verbose_name='执法权限')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    equipment_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='执法设备编号')

    class Meta:
        db_table = 'law_enforcer'
        managed = False
        verbose_name = '执法人员'
        verbose_name_plural = '执法人员'
        indexes = [
            models.Index(fields=['department'], name='idx_enforcer_department'),
        ]

    def __str__(self):
        return f"{self.enforcer_name} ({self.department})"


class SurveillancePoint(models.Model):
    """视频监控点表"""
    STATUS_CHOICES = [
        ('正常', '正常'),
        ('故障', '故障'),
    ]

    monitor_id = models.CharField(max_length=20, primary_key=True, verbose_name='监控点编号')
    area = models.ForeignKey(FunctionalArea, on_delete=models.CASCADE, db_column='area_id', verbose_name='部署区域')
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='位置经度')
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='位置纬度')
    monitoring_range = models.TextField(blank=True, null=True, verbose_name='监控范围')
    device_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='设备状态')
    storage_period = models.IntegerField(
        default=90,
        validators=[MinValueValidator(1)],
        verbose_name='存储周期(天)'
    )

    class Meta:
        db_table = 'surveillance_point'
        managed = False
        verbose_name = '视频监控点'
        verbose_name_plural = '视频监控点'
        indexes = [
            models.Index(fields=['area'], name='idx_surveillance_area'),
            models.Index(fields=['device_status'], name='idx_surveillance_status'),
        ]

    def __str__(self):
        return f"{self.monitor_id} - {self.area.area_name}"


class IllegalBehavior(models.Model):
    """非法行为记录表"""
    STATUS_CHOICES = [
        ('未处理', '未处理'),
        ('处理中', '处理中'),
        ('已结案', '已结案'),
    ]

    record_id = models.CharField(max_length=30, primary_key=True, verbose_name='记录编号')
    behavior_type = models.CharField(max_length=50, verbose_name='行为类型')
    occurrence_time = models.DateTimeField(verbose_name='发生时间')
    area = models.ForeignKey(FunctionalArea, on_delete=models.CASCADE, db_column='area_id', verbose_name='发生区域')
    evidence_path = models.CharField(max_length=255, verbose_name='证据路径')
    handling_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='处理状态')
    enforcer = models.ForeignKey(
        LawEnforcer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column='enforcer_id',
        verbose_name='执法人员'
    )
    handling_result = models.TextField(blank=True, null=True, verbose_name='处理结果')
    penalty_basis = models.TextField(blank=True, null=True, verbose_name='处罚依据')

    class Meta:
        db_table = 'illegal_behavior'
        managed = False
        verbose_name = '非法行为记录'
        verbose_name_plural = '非法行为记录'
        indexes = [
            models.Index(fields=['occurrence_time'], name='idx_illegal_time'),
            models.Index(fields=['handling_status'], name='idx_illegal_status'),
            models.Index(fields=['enforcer'], name='idx_illegal_enforcer'),
            models.Index(fields=['area'], name='idx_illegal_area'),
        ]

    def __str__(self):
        return f"{self.behavior_type} - {self.occurrence_time}"


class EnforcementDispatch(models.Model):
    """执法调度表"""
    STATUS_CHOICES = [
        ('待响应', '待响应'),
        ('已派单', '已派单'),
        ('已完成', '已完成'),
    ]

    dispatch_id = models.CharField(max_length=30, primary_key=True, verbose_name='调度编号')
    record = models.ForeignKey(IllegalBehavior, on_delete=models.CASCADE, db_column='record_id', verbose_name='非法行为记录')
    enforcer = models.ForeignKey(LawEnforcer, on_delete=models.CASCADE, db_column='enforcer_id', verbose_name='执法人员')
    dispatch_time = models.DateTimeField(verbose_name='调度时间')
    response_time = models.DateTimeField(blank=True, null=True, verbose_name='响应时间')
    completion_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    dispatch_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='调度状态')

    class Meta:
        db_table = 'enforcement_dispatch'
        managed = False
        verbose_name = '执法调度'
        verbose_name_plural = '执法调度'
        indexes = [
            models.Index(fields=['record'], name='idx_dispatch_record'),
            models.Index(fields=['enforcer'], name='idx_dispatch_enforcer'),
            models.Index(fields=['dispatch_status'], name='idx_dispatch_status'),
            models.Index(fields=['dispatch_time'], name='idx_dispatch_time'),
        ]

    def __str__(self):
        return f"{self.dispatch_id} - {self.dispatch_status}"


class ResearchProject(models.Model):
    """科研项目表"""
    STATUS_CHOICES = [
        ('在研', '在研'),
        ('已结题', '已结题'),
        ('暂停', '暂停'),
    ]

    project_id = models.CharField(max_length=20, primary_key=True, verbose_name='项目编号')
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    principal = models.ForeignKey(SystemUser, on_delete=models.CASCADE, db_column='principal_id', verbose_name='负责人')
    applicant_unit = models.CharField(max_length=100, verbose_name='申请单位')
    start_date = models.DateField(verbose_name='立项日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结题日期')
    project_status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='项目状态')
    research_field = models.CharField(max_length=50, verbose_name='研究领域')

    class Meta:
        db_table = 'research_project'
        managed = False
        verbose_name = '科研项目'
        verbose_name_plural = '科研项目'
        indexes = [
            models.Index(fields=['principal'], name='idx_project_principal'),
            models.Index(fields=['project_status'], name='idx_project_status'),
            models.Index(fields=['research_field'], name='idx_project_field'),
        ]

    def __str__(self):
        return f"{self.project_name} ({self.project_status})"


class ResearchDataCollection(models.Model):
    """科研数据采集记录表"""
    SOURCE_CHOICES = [
        ('实地采集', '实地采集'),
        ('系统调用', '系统调用'),
    ]

    collection_id = models.CharField(max_length=30, primary_key=True, verbose_name='采集编号')
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, db_column='project_id', verbose_name='项目')
    collector = models.ForeignKey(SystemUser, on_delete=models.CASCADE, db_column='collector_id', verbose_name='采集人')
    collection_time = models.DateTimeField(verbose_name='采集时间')
    area = models.ForeignKey(FunctionalArea, on_delete=models.CASCADE, db_column='area_id', verbose_name='区域')
    collection_content = models.TextField(verbose_name='采集内容')
    sample_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='样本编号')
    monitoring_data_id = models.CharField(max_length=30, blank=True, null=True, verbose_name='监测数据编号')
    survey_record = models.TextField(blank=True, null=True, verbose_name='调查记录')
    data_source = models.CharField(max_length=20, choices=SOURCE_CHOICES, verbose_name='数据来源')

    class Meta:
        db_table = 'research_data_collection'
        managed = False
        verbose_name = '科研数据采集记录'
        verbose_name_plural = '科研数据采集记录'
        indexes = [
            models.Index(fields=['project'], name='idx_research_project'),
            models.Index(fields=['collector'], name='idx_research_collector'),
            models.Index(fields=['collection_time'], name='idx_research_time'),
            models.Index(fields=['area'], name='idx_research_area'),
        ]

    def __str__(self):
        return f"{self.project.project_name} - {self.collection_time}"


class ResearchAchievement(models.Model):
    """科研成果表"""
    TYPE_CHOICES = [
        ('论文', '论文'),
        ('报告', '报告'),
        ('专利', '专利'),
        ('其他', '其他'),
    ]

    PERMISSION_CHOICES = [
        ('公开', '公开'),
        ('内部共享', '内部共享'),
        ('保密', '保密'),
    ]

    achievement_id = models.CharField(max_length=30, primary_key=True, verbose_name='成果编号')
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, db_column='project_id', verbose_name='项目')
    achievement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='成果类型')
    achievement_name = models.CharField(max_length=200, verbose_name='成果名称')
    publish_date = models.DateField(verbose_name='发表日期')
    share_permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, verbose_name='共享权限')
    file_path = models.CharField(max_length=255, blank=True, null=True, verbose_name='文件路径')

    class Meta:
        db_table = 'research_achievement'
        managed = False
        verbose_name = '科研成果'
        verbose_name_plural = '科研成果'
        indexes = [
            models.Index(fields=['project'], name='idx_achievement_project'),
            models.Index(fields=['achievement_type'], name='idx_achievement_type'),
            models.Index(fields=['share_permission'], name='idx_achievement_permission'),
        ]

    def __str__(self):
        return f"{self.achievement_name} ({self.achievement_type})"
