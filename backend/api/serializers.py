"""
DRF Serializers for National Park Management System
Organized by business lines:
1. Biodiversity Monitoring (生物多样性监测)
2. Environmental Monitoring (生态环境监测)
3. Visitor Management (游客智能管理)
4. Law Enforcement (执法监管)
5. Research Support (科研数据支撑)
"""
from rest_framework import serializers
from . import models


# ============================================================================
# Base & Common Serializers
# ============================================================================

class FunctionalAreaSerializer(serializers.ModelSerializer):
    """功能分区序列化器"""
    class Meta:
        model = models.FunctionalArea
        fields = '__all__'


class SystemUserSerializer(serializers.ModelSerializer):
    """系统用户序列化器"""
    class Meta:
        model = models.SystemUser
        fields = ['user_id', 'username', 'real_name', 'contact_phone',
                  'role_type', 'account_status', 'create_time', 'last_login_time']
        read_only_fields = ['create_time', 'last_login_time', 'failed_login_count']


class SystemUserDetailSerializer(serializers.ModelSerializer):
    """系统用户详情序列化器(包含敏感信息)"""
    class Meta:
        model = models.SystemUser
        fields = '__all__'
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }


class UserSessionSerializer(serializers.ModelSerializer):
    """用户会话序列化器"""
    user_info = SystemUserSerializer(source='user', read_only=True)

    class Meta:
        model = models.UserSession
        fields = '__all__'
        read_only_fields = ['login_time', 'last_activity_time']


# ============================================================================
# Biodiversity Monitoring (生物多样性监测)
# ============================================================================

class SpeciesSerializer(serializers.ModelSerializer):
    """物种序列化器"""
    class Meta:
        model = models.Species
        fields = '__all__'


class SpeciesListSerializer(serializers.ModelSerializer):
    """物种列表序列化器(简化版)"""
    class Meta:
        model = models.Species
        fields = ['species_id', 'chinese_name', 'latin_name', 'protection_level']


class HabitatSerializer(serializers.ModelSerializer):
    """栖息地序列化器"""
    class Meta:
        model = models.Habitat
        fields = '__all__'


class HabitatSpeciesSerializer(serializers.ModelSerializer):
    """栖息地物种关联序列化器"""
    habitat_info = HabitatSerializer(source='habitat', read_only=True)
    species_info = SpeciesListSerializer(source='species', read_only=True)

    class Meta:
        model = models.HabitatSpecies
        fields = '__all__'


class MonitoringDeviceSerializer(serializers.ModelSerializer):
    """监测设备序列化器"""
    deployment_area_info = FunctionalAreaSerializer(source='deployment_area', read_only=True)

    class Meta:
        model = models.MonitoringDevice
        fields = '__all__'


class MonitoringRecordSerializer(serializers.ModelSerializer):
    """监测记录序列化器"""
    species_info = SpeciesListSerializer(source='species', read_only=True)
    device_info = MonitoringDeviceSerializer(source='device', read_only=True)
    recorder_info = SystemUserSerializer(source='recorder', read_only=True)

    class Meta:
        model = models.MonitoringRecord
        fields = '__all__'


class MonitoringRecordCreateSerializer(serializers.ModelSerializer):
    """监测记录创建序列化器"""
    class Meta:
        model = models.MonitoringRecord
        fields = '__all__'


# ============================================================================
# Environmental Monitoring (生态环境监测)
# ============================================================================

class MonitoringIndicatorSerializer(serializers.ModelSerializer):
    """监测指标序列化器"""
    class Meta:
        model = models.MonitoringIndicator
        fields = '__all__'


class EnvironmentalDataSerializer(serializers.ModelSerializer):
    """环境监测数据序列化器"""
    indicator_info = MonitoringIndicatorSerializer(source='indicator', read_only=True)
    device_info = MonitoringDeviceSerializer(source='device', read_only=True)
    area_info = FunctionalAreaSerializer(source='area', read_only=True)

    class Meta:
        model = models.EnvironmentalData
        fields = '__all__'


class EnvironmentalDataCreateSerializer(serializers.ModelSerializer):
    """环境监测数据创建序列化器"""
    class Meta:
        model = models.EnvironmentalData
        fields = '__all__'


class EnvironmentalDataStatsSerializer(serializers.Serializer):
    """环境数据统计序列化器"""
    indicator_name = serializers.CharField()
    avg_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()


# ============================================================================
# Visitor Management (游客智能管理)
# ============================================================================

class VisitorSerializer(serializers.ModelSerializer):
    """游客序列化器"""
    class Meta:
        model = models.Visitor
        fields = '__all__'


class VisitorListSerializer(serializers.ModelSerializer):
    """游客列表序列化器(简化版,隐藏敏感信息)"""
    class Meta:
        model = models.Visitor
        fields = ['visitor_id', 'visitor_name', 'contact_phone',
                  'entry_time', 'exit_time', 'entry_method']


class ReservationSerializer(serializers.ModelSerializer):
    """预约记录序列化器"""
    visitor_info = VisitorListSerializer(source='visitor', read_only=True)

    class Meta:
        model = models.Reservation
        fields = '__all__'


class ReservationCreateSerializer(serializers.ModelSerializer):
    """预约记录创建序列化器"""
    class Meta:
        model = models.Reservation
        fields = '__all__'

    def validate(self, data):
        """验证预约数据"""
        if data['party_size'] <= 0:
            raise serializers.ValidationError("同行人数必须大于0")
        if data['ticket_amount'] < 0:
            raise serializers.ValidationError("购票金额不能为负数")
        return data


class VisitorTrajectorySerializer(serializers.ModelSerializer):
    """游客轨迹序列化器"""
    visitor_info = VisitorListSerializer(source='visitor', read_only=True)
    area_info = FunctionalAreaSerializer(source='area', read_only=True)

    class Meta:
        model = models.VisitorTrajectory
        fields = '__all__'


class TrafficControlSerializer(serializers.ModelSerializer):
    """流量控制序列化器"""
    area_info = FunctionalAreaSerializer(source='area', read_only=True)

    class Meta:
        model = models.TrafficControl
        fields = '__all__'


class TrafficControlStatsSerializer(serializers.Serializer):
    """流量控制统计序列化器"""
    area_name = serializers.CharField()
    utilization_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    current_visitor_count = serializers.IntegerField()
    daily_capacity = serializers.IntegerField()
    current_status = serializers.CharField()


# ============================================================================
# Law Enforcement (执法监管)
# ============================================================================

class LawEnforcerSerializer(serializers.ModelSerializer):
    """执法人员序列化器"""
    class Meta:
        model = models.LawEnforcer
        fields = '__all__'


class SurveillancePointSerializer(serializers.ModelSerializer):
    """视频监控点序列化器"""
    area_info = FunctionalAreaSerializer(source='area', read_only=True)

    class Meta:
        model = models.SurveillancePoint
        fields = '__all__'


class IllegalBehaviorSerializer(serializers.ModelSerializer):
    """非法行为记录序列化器"""
    area_info = FunctionalAreaSerializer(source='area', read_only=True)
    enforcer_info = LawEnforcerSerializer(source='enforcer', read_only=True)

    class Meta:
        model = models.IllegalBehavior
        fields = '__all__'


class IllegalBehaviorCreateSerializer(serializers.ModelSerializer):
    """非法行为记录创建序列化器"""
    class Meta:
        model = models.IllegalBehavior
        fields = '__all__'


class EnforcementDispatchSerializer(serializers.ModelSerializer):
    """执法调度序列化器"""
    record_info = IllegalBehaviorSerializer(source='record', read_only=True)
    enforcer_info = LawEnforcerSerializer(source='enforcer', read_only=True)

    class Meta:
        model = models.EnforcementDispatch
        fields = '__all__'

    def validate(self, data):
        """验证调度数据"""
        if data.get('response_time') and data.get('dispatch_time'):
            if data['response_time'] < data['dispatch_time']:
                raise serializers.ValidationError("响应时间不能早于调度时间")
        if data.get('completion_time') and data.get('response_time'):
            if data['completion_time'] < data['response_time']:
                raise serializers.ValidationError("完成时间不能早于响应时间")
        return data


class EnforcementDispatchCreateSerializer(serializers.ModelSerializer):
    """执法调度创建序列化器"""
    class Meta:
        model = models.EnforcementDispatch
        fields = '__all__'


# ============================================================================
# Research Support (科研数据支撑)
# ============================================================================

class ResearchProjectSerializer(serializers.ModelSerializer):
    """科研项目序列化器"""
    principal_info = SystemUserSerializer(source='principal', read_only=True)

    class Meta:
        model = models.ResearchProject
        fields = '__all__'

    def validate(self, data):
        """验证项目数据"""
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("结题日期不能早于立项日期")
        return data


class ResearchProjectCreateSerializer(serializers.ModelSerializer):
    """科研项目创建序列化器"""
    class Meta:
        model = models.ResearchProject
        fields = '__all__'


class ResearchDataCollectionSerializer(serializers.ModelSerializer):
    """科研数据采集记录序列化器"""
    project_info = ResearchProjectSerializer(source='project', read_only=True)
    collector_info = SystemUserSerializer(source='collector', read_only=True)
    area_info = FunctionalAreaSerializer(source='area', read_only=True)

    class Meta:
        model = models.ResearchDataCollection
        fields = '__all__'


class ResearchDataCollectionCreateSerializer(serializers.ModelSerializer):
    """科研数据采集记录创建序列化器"""
    class Meta:
        model = models.ResearchDataCollection
        fields = '__all__'


class ResearchAchievementSerializer(serializers.ModelSerializer):
    """科研成果序列化器"""
    project_info = ResearchProjectSerializer(source='project', read_only=True)

    class Meta:
        model = models.ResearchAchievement
        fields = '__all__'


class ResearchAchievementCreateSerializer(serializers.ModelSerializer):
    """科研成果创建序列化器"""
    class Meta:
        model = models.ResearchAchievement
        fields = '__all__'


# ============================================================================
# Statistics & Analytics Serializers
# ============================================================================

class BiodiversityStatsSerializer(serializers.Serializer):
    """生物多样性统计序列化器"""
    total_species = serializers.IntegerField()
    protected_species_count = serializers.IntegerField()
    monitoring_records_count = serializers.IntegerField()
    active_devices = serializers.IntegerField()


class VisitorStatsSerializer(serializers.Serializer):
    """游客统计序列化器"""
    total_visitors = serializers.IntegerField()
    online_reservations = serializers.IntegerField()
    offline_purchases = serializers.IntegerField()
    current_in_park = serializers.IntegerField()


class EnforcementStatsSerializer(serializers.Serializer):
    """执法统计序列化器"""
    total_illegal_behaviors = serializers.IntegerField()
    unhandled_count = serializers.IntegerField()
    in_progress_count = serializers.IntegerField()
    closed_count = serializers.IntegerField()
    avg_response_time = serializers.FloatField()


class ResearchStatsSerializer(serializers.Serializer):
    """科研统计序列化器"""
    total_projects = serializers.IntegerField()
    ongoing_projects = serializers.IntegerField()
    completed_projects = serializers.IntegerField()
    total_achievements = serializers.IntegerField()
    public_achievements = serializers.IntegerField()
