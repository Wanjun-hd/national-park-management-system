"""
API Views for National Park Management System
国家公园管理系统 API 视图
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db.models import Count, Avg, Max, Min, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import hashlib
from datetime import datetime, timedelta
from . import models, serializers, exceptions, validators


# ============================================================================
# 认证相关API
# ============================================================================

@extend_schema(
    tags=['认证'],
    summary='用户登录',
    description='系统用户登录接口，支持SHA-256密码加密和账号锁定机制',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'description': '用户名'},
                'password': {'type': 'string', 'description': '密码'},
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'description': '登录成功',
            'content': {
                'application/json': {
                    'example': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'user': {
                            'user_id': 'U001',
                            'username': 'admin',
                            'real_name': '系统管理员',
                            'role_type': '系统管理员',
                        }
                    }
                }
            }
        },
        400: {'description': '请求参数错误'},
        401: {'description': '密码错误'},
        403: {'description': '账号被锁定或停用'},
        404: {'description': '用户不存在'},
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': '请提供用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = models.SystemUser.objects.get(username=username)

        # 检查账号状态
        if user.account_status == '锁定':
            raise exceptions.AccountLockedException(username)

        if user.account_status == '停用':
            raise exceptions.AccountDisabledException(username)

        # 验证密码
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if user.password_hash != password_hash:
            user.failed_login_count += 1
            user.last_failed_login_time = datetime.now()

            if user.failed_login_count >= 5:
                user.account_status = '锁定'
                user.save()
                raise exceptions.AccountLockedException(username)

            user.save()
            remaining = 5 - user.failed_login_count
            raise exceptions.InvalidPasswordException(remaining)

        # 登录成功，重置失败次数
        user.failed_login_count = 0
        user.last_login_time = datetime.now()
        user.save()

        # 生成JWT token
        refresh = RefreshToken()
        refresh['user_id'] = user.user_id
        refresh['username'] = user.username
        refresh['role_type'] = user.role_type

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'real_name': user.real_name,
                'role_type': user.role_type,
                'contact_phone': user.contact_phone,
                'account_status': user.account_status,
            }
        }, status=status.HTTP_200_OK)

    except models.SystemUser.DoesNotExist:
        return Response({'detail': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """用户登出(前端清理token即可)"""
    return Response({'detail': 'logout success'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def current_user_view(request):
    """获取当前用户信息"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return Response({'detail': '未提供认证信息'}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ', 1)[1]
    try:
        access = AccessToken(token)
        user_id = access.get('user_id')
        if not user_id:
            return Response({'detail': '无效token'}, status=status.HTTP_401_UNAUTHORIZED)
        user = models.SystemUser.objects.get(user_id=user_id)
        return Response({
            'user_id': user.user_id,
            'username': user.username,
            'real_name': user.real_name,
            'role_type': user.role_type,
            'contact_phone': user.contact_phone,
            'account_status': user.account_status,
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({'detail': '无效token'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_test_user(request):
    """创建测试用户"""
    try:
        users_created = []
        users_updated = []

        # 管理员
        admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
        admin, created = models.SystemUser.objects.update_or_create(
            user_id='U001',
            defaults={
                'username': 'admin',
                'password_hash': admin_password,
                'real_name': '系统管理员',
                'contact_phone': '13800138000',
                'role_type': '系统管理员',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('admin')

        # 生态监测员
        monitor_password = hashlib.sha256('monitor123'.encode()).hexdigest()
        monitor, created = models.SystemUser.objects.update_or_create(
            user_id='U002',
            defaults={
                'username': 'monitor',
                'password_hash': monitor_password,
                'real_name': '张三',
                'contact_phone': '13800138001',
                'role_type': '生态监测员',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('monitor')

        # 数据分析师
        analyst_password = hashlib.sha256('analyst123'.encode()).hexdigest()
        analyst, created = models.SystemUser.objects.update_or_create(
            user_id='U003',
            defaults={
                'username': 'analyst',
                'password_hash': analyst_password,
                'real_name': '李四',
                'contact_phone': '13800138002',
                'role_type': '数据分析师',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('analyst')

        # 游客
        visitor_password = hashlib.sha256('visitor123'.encode()).hexdigest()
        visitor, created = models.SystemUser.objects.update_or_create(
            user_id='U004',
            defaults={
                'username': 'visitor',
                'password_hash': visitor_password,
                'real_name': '王五',
                'contact_phone': '13800138003',
                'role_type': '游客',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('visitor')

        # 执法人员
        enforcer_password = hashlib.sha256('enforcer123'.encode()).hexdigest()
        enforcer, created = models.SystemUser.objects.update_or_create(
            user_id='U005',
            defaults={
                'username': 'enforcer',
                'password_hash': enforcer_password,
                'real_name': '赵六',
                'contact_phone': '13800138004',
                'role_type': '执法人员',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('enforcer')

        # 科研人员
        researcher_password = hashlib.sha256('researcher123'.encode()).hexdigest()
        researcher, created = models.SystemUser.objects.update_or_create(
            user_id='U006',
            defaults={
                'username': 'researcher',
                'password_hash': researcher_password,
                'real_name': '钱七',
                'contact_phone': '13800138005',
                'role_type': '科研人员',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('researcher')

        # 公园管理人员
        manager_password = hashlib.sha256('manager123'.encode()).hexdigest()
        manager, created = models.SystemUser.objects.update_or_create(
            user_id='U007',
            defaults={
                'username': 'manager',
                'password_hash': manager_password,
                'real_name': '孙八',
                'contact_phone': '13800138006',
                'role_type': '公园管理人员',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('manager')

        # 技术人员
        tech_password = hashlib.sha256('tech123'.encode()).hexdigest()
        tech, created = models.SystemUser.objects.update_or_create(
            user_id='U008',
            defaults={
                'username': 'tech',
                'password_hash': tech_password,
                'real_name': '周九',
                'contact_phone': '13800138007',
                'role_type': '技术人员',
                'account_status': '正常',
                'failed_login_count': 0,
            }
        )
        (users_created if created else users_updated).append('tech')

        return Response({
            'detail': '测试用户创建成功',
            'created': users_created,
            'updated': users_updated,
            'users': [
                {'username': 'admin', 'password': 'admin123', 'role': '系统管理员'},
                {'username': 'monitor', 'password': 'monitor123', 'role': '生态监测员'},
                {'username': 'analyst', 'password': 'analyst123', 'role': '数据分析师'},
                {'username': 'visitor', 'password': 'visitor123', 'role': '游客'},
                {'username': 'enforcer', 'password': 'enforcer123', 'role': '执法人员'},
                {'username': 'researcher', 'password': 'researcher123', 'role': '科研人员'},
                {'username': 'manager', 'password': 'manager123', 'role': '公园管理人员'},
                {'username': 'tech', 'password': 'tech123', 'role': '技术人员'},
            ]
        })

    except Exception as e:
        return Response({'detail': f'创建失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# 生物多样性监测 ViewSets
# ============================================================================

@extend_schema_view(
    list=extend_schema(tags=['生物多样性'], summary='获取物种列表', description='支持分页、筛选和搜索'),
    retrieve=extend_schema(tags=['生物多样性'], summary='获取物种详情'),
    create=extend_schema(tags=['生物多样性'], summary='创建物种记录'),
    update=extend_schema(tags=['生物多样性'], summary='更新物种信息'),
    partial_update=extend_schema(tags=['生物多样性'], summary='部分更新物种信息'),
    destroy=extend_schema(tags=['生物多样性'], summary='删除物种记录'),
)
class SpeciesViewSet(viewsets.ModelViewSet):
    """
    物种管理ViewSet

    提供物种的CRUD操作，支持按保护级别筛选和搜索
    """
    queryset = models.Species.objects.all()
    serializer_class = serializers.SpeciesSerializer
    permission_classes = [AllowAny]  # 开发阶段暂时允许所有访问
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['protection_level', 'kingdom', 'phylum']
    search_fields = ['chinese_name', 'latin_name']
    ordering_fields = ['species_id', 'chinese_name']

    @extend_schema(
        tags=['生物多样性'],
        summary='获取受保护物种列表',
        description='获取所有保护级别不为"无"的物种',
        responses={200: serializers.SpeciesSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def protected(self, request):
        """获取受保护物种列表"""
        protected_species = self.queryset.exclude(protection_level='无')
        serializer = self.get_serializer(protected_species, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['生物多样性'],
        summary='获取物种统计信息',
        description='统计各保护级别的物种数量',
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取物种统计信息"""
        stats = {
            'total': self.queryset.count(),
            'by_protection_level': {},
            'by_kingdom': {}
        }

        # 按保护级别统计
        protection_stats = self.queryset.values('protection_level').annotate(count=Count('species_id'))
        for item in protection_stats:
            stats['by_protection_level'][item['protection_level']] = item['count']

        # 按界统计
        kingdom_stats = self.queryset.values('kingdom').annotate(count=Count('species_id'))
        for item in kingdom_stats:
            stats['by_kingdom'][item['kingdom']] = item['count']

        return Response(stats)


class HabitatViewSet(viewsets.ModelViewSet):
    """栖息地管理ViewSet"""
    queryset = models.Habitat.objects.all()
    serializer_class = serializers.HabitatSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ecology_type']
    search_fields = ['area_name']


class MonitoringDeviceViewSet(viewsets.ModelViewSet):
    """监测设备ViewSet"""
    queryset = models.MonitoringDevice.objects.all()
    serializer_class = serializers.MonitoringDeviceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation_status', 'device_type']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新设备状态"""
        device = self.get_object()
        new_status = request.data.get('operation_status')

        if new_status not in ['正常', '故障', '离线']:
            return Response({'detail': '无效的状态值'}, status=status.HTTP_400_BAD_REQUEST)

        device.operation_status = new_status
        device.save()

        return Response({'detail': '设备状态更新成功', 'operation_status': new_status})


class MonitoringRecordViewSet(viewsets.ModelViewSet):
    """监测记录ViewSet"""
    queryset = models.MonitoringRecord.objects.all().select_related('species', 'device', 'recorder')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['species', 'monitoring_method', 'data_status']
    ordering_fields = ['monitoring_time']
    ordering = ['-monitoring_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MonitoringRecordCreateSerializer
        return serializers.MonitoringRecordSerializer


# ============================================================================
# 环境监测 ViewSets
# ============================================================================

class MonitoringIndicatorViewSet(viewsets.ModelViewSet):
    """监测指标ViewSet"""
    queryset = models.MonitoringIndicator.objects.all()
    serializer_class = serializers.MonitoringIndicatorSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['indicator_name']


class EnvironmentalDataViewSet(viewsets.ModelViewSet):
    """环境数据ViewSet"""
    queryset = models.EnvironmentalData.objects.all().select_related('indicator', 'device', 'area')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['indicator', 'area', 'data_quality']
    ordering_fields = ['collection_time']
    ordering = ['-collection_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EnvironmentalDataCreateSerializer
        return serializers.EnvironmentalDataSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """环境数据统计"""
        indicator_id = request.query_params.get('indicator_id')

        if not indicator_id:
            return Response({'detail': '请提供indicator_id参数'}, status=status.HTTP_400_BAD_REQUEST)

        stats = models.EnvironmentalData.objects.filter(
            indicator_id=indicator_id
        ).aggregate(
            avg_value=Avg('monitoring_value'),
            max_value=Max('monitoring_value'),
            min_value=Min('monitoring_value'),
            count=Count('data_id')
        )

        indicator = models.MonitoringIndicator.objects.get(indicator_id=indicator_id)
        stats['indicator_name'] = indicator.indicator_name

        return Response(stats)


# ============================================================================
# 游客管理 ViewSets
# ============================================================================

class VisitorViewSet(viewsets.ModelViewSet):
    """游客管理ViewSet"""
    queryset = models.Visitor.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['visitor_name', 'id_card_number', 'contact_phone']
    ordering_fields = ['entry_time']
    ordering = ['-entry_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.VisitorListSerializer
        return serializers.VisitorSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """预约管理ViewSet"""
    queryset = models.Reservation.objects.all().select_related('visitor')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['reservation_status', 'payment_status']
    ordering_fields = ['reservation_date']
    ordering = ['-reservation_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ReservationCreateSerializer
        return serializers.ReservationSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        reservation = self.get_object()

        if reservation.reservation_status == '已完成':
            return Response({'detail': '已完成的预约无法取消'}, status=status.HTTP_400_BAD_REQUEST)

        reservation.reservation_status = '已取消'
        reservation.save()

        return Response({'detail': '预约已取消'})


class TrafficControlViewSet(viewsets.ModelViewSet):
    """流量控制ViewSet"""
    queryset = models.TrafficControl.objects.all().select_related('area')
    serializer_class = serializers.TrafficControlSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area', 'current_status']

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """流量统计"""
        controls = self.queryset.all()
        stats = []

        for control in controls:
            utilization_rate = (control.current_visitor_count / control.daily_capacity * 100) if control.daily_capacity > 0 else 0
            stats.append({
                'area_name': control.area.area_name,
                'utilization_rate': round(utilization_rate, 2),
                'current_visitor_count': control.current_visitor_count,
                'daily_capacity': control.daily_capacity,
                'current_status': control.current_status
            })

        return Response(stats)


# ============================================================================
# 执法监管 ViewSets
# ============================================================================

class IllegalBehaviorViewSet(viewsets.ModelViewSet):
    """非法行为管理ViewSet"""
    queryset = models.IllegalBehavior.objects.all().select_related('area', 'enforcer')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['handling_status', 'area']
    ordering_fields = ['occurrence_time']
    ordering = ['-occurrence_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.IllegalBehaviorCreateSerializer
        return serializers.IllegalBehaviorSerializer

    @action(detail=True, methods=['post'])
    def handle(self, request, pk=None):
        """处理非法行为"""
        behavior = self.get_object()

        handling_result = request.data.get('handling_result')
        penalty_basis = request.data.get('penalty_basis')
        enforcer_id = request.data.get('enforcer_id')

        behavior.handling_result = handling_result
        behavior.penalty_basis = penalty_basis
        behavior.enforcer_id = enforcer_id
        behavior.handling_status = '已结案'
        behavior.save()

        return Response({'detail': '处理完成'})


class EnforcementDispatchViewSet(viewsets.ModelViewSet):
    """执法调度ViewSet"""
    queryset = models.EnforcementDispatch.objects.all().select_related('record', 'enforcer')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dispatch_status', 'enforcer']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.EnforcementDispatchCreateSerializer
        return serializers.EnforcementDispatchSerializer

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """响应调度"""
        dispatch = self.get_object()
        dispatch.response_time = request.data.get('response_time') or timezone.now()
        dispatch.dispatch_status = '已派单'
        dispatch.save()
        return Response(serializers.EnforcementDispatchSerializer(dispatch).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成调度"""
        dispatch = self.get_object()
        dispatch.completion_time = request.data.get('completion_time') or timezone.now()
        dispatch.dispatch_status = '已完成'
        dispatch.save()
        return Response(serializers.EnforcementDispatchSerializer(dispatch).data)


# ============================================================================
# 科研支撑 ViewSets
# ============================================================================

class ResearchProjectViewSet(viewsets.ModelViewSet):
    """科研项目ViewSet"""
    queryset = models.ResearchProject.objects.all().select_related('principal')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['project_status', 'research_field']
    search_fields = ['project_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ResearchProjectCreateSerializer
        return serializers.ResearchProjectSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """结题项目"""
        project = self.get_object()
        project.project_status = '已结题'
        if not project.end_date:
            project.end_date = timezone.now().date()
        project.save()
        return Response(serializers.ResearchProjectSerializer(project).data)

    @action(detail=True, methods=['get'])
    def data_collections(self, request, pk=None):
        """项目数据采集记录"""
        project = self.get_object()
        queryset = models.ResearchDataCollection.objects.filter(project=project).select_related('project', 'collector', 'area')
        serializer = serializers.ResearchDataCollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def achievements(self, request, pk=None):
        """项目成果列表"""
        project = self.get_object()
        queryset = models.ResearchAchievement.objects.filter(project=project).select_related('project')
        serializer = serializers.ResearchAchievementSerializer(queryset, many=True)
        return Response(serializer.data)


class ResearchDataCollectionViewSet(viewsets.ModelViewSet):
    """科研数据采集ViewSet"""
    queryset = models.ResearchDataCollection.objects.all().select_related('project', 'collector', 'area')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'data_source']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ResearchDataCollectionCreateSerializer
        return serializers.ResearchDataCollectionSerializer


class ResearchAchievementViewSet(viewsets.ModelViewSet):
    """科研成果ViewSet"""
    queryset = models.ResearchAchievement.objects.all().select_related('project')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['achievement_type', 'share_permission']

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ResearchAchievementCreateSerializer
        return serializers.ResearchAchievementSerializer


# ============================================================================
# 统计分析API
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    """仪表盘统计数据"""
    stats = {
        'biodiversity': {
            'total_species': models.Species.objects.count(),
            'protected_species': models.Species.objects.exclude(protection_level='无').count(),
            'monitoring_records': models.MonitoringRecord.objects.count(),
            'active_devices': models.MonitoringDevice.objects.filter(operation_status='正常').count(),
        },
        'environment': {
            'total_indicators': models.MonitoringIndicator.objects.count(),
            'total_data_points': models.EnvironmentalData.objects.count(),
            'devices': models.MonitoringDevice.objects.count(),
        },
        'visitor': {
            'total_visitors': models.Visitor.objects.count(),
            'current_in_park': models.Visitor.objects.filter(
                entry_time__isnull=False,
                exit_time__isnull=True
            ).count(),
            'reservations_today': models.Reservation.objects.filter(
                reservation_date=datetime.now().date()
            ).count(),
        },
        'enforcement': {
            'total_illegal_behaviors': models.IllegalBehavior.objects.count(),
            'unhandled': models.IllegalBehavior.objects.filter(handling_status='未处理').count(),
            'in_progress': models.IllegalBehavior.objects.filter(handling_status='处理中').count(),
        },
        'research': {
            'total_projects': models.ResearchProject.objects.count(),
            'ongoing_projects': models.ResearchProject.objects.filter(project_status='在研').count(),
            'total_achievements': models.ResearchAchievement.objects.count(),
        }
    }

    return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def biodiversity_stats(request):
    """生物多样性统计"""
    stats = {
        'total_species': models.Species.objects.count(),
        'protected_species_count': models.Species.objects.exclude(protection_level='无').count(),
        'monitoring_records_count': models.MonitoringRecord.objects.count(),
        'active_devices': models.MonitoringDevice.objects.filter(operation_status='正常').count(),
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def visitor_stats(request):
    """游客统计"""
    stats = {
        'total_visitors': models.Visitor.objects.count(),
        'online_reservations': models.Visitor.objects.filter(entry_method='线上预约').count(),
        'offline_purchases': models.Visitor.objects.filter(entry_method='现场购票').count(),
        'current_in_park': models.Visitor.objects.filter(
            entry_time__isnull=False,
            exit_time__isnull=True
        ).count(),
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def enforcement_stats(request):
    """执法统计"""
    dispatches = models.EnforcementDispatch.objects.exclude(
        response_time__isnull=True,
        dispatch_time__isnull=True
    ).values_list('dispatch_time', 'response_time')
    total_seconds = sum(
        (response_time - dispatch_time).total_seconds()
        for dispatch_time, response_time in dispatches
    )
    count = dispatches.count()
    avg_response_time = total_seconds / count if count else 0

    stats = {
        'total_illegal_behaviors': models.IllegalBehavior.objects.count(),
        'unhandled_count': models.IllegalBehavior.objects.filter(handling_status='未处理').count(),
        'in_progress_count': models.IllegalBehavior.objects.filter(handling_status='处理中').count(),
        'closed_count': models.IllegalBehavior.objects.filter(handling_status='已结案').count(),
        'avg_response_time': avg_response_time,
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def research_stats(request):
    """科研统计"""
    stats = {
        'total_projects': models.ResearchProject.objects.count(),
        'ongoing_projects': models.ResearchProject.objects.filter(project_status='在研').count(),
        'completed_projects': models.ResearchProject.objects.filter(project_status='已结题').count(),
        'total_achievements': models.ResearchAchievement.objects.count(),
        'public_achievements': models.ResearchAchievement.objects.filter(share_permission='公开').count(),
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    """测试API"""
    return Response({
        'status': 'success',
        'message': '后端API正常运行',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


# ============================================================================
# 补充缺失的 ViewSets
# ============================================================================

class VisitorTrajectoryViewSet(viewsets.ModelViewSet):
    """游客轨迹ViewSet"""
    queryset = models.VisitorTrajectory.objects.all().select_related('visitor', 'area')
    serializer_class = serializers.VisitorTrajectorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['visitor', 'area']

    @action(detail=False, methods=['get'], url_path='by-visitor/(?P<visitor_id>[^/.]+)')
    def by_visitor(self, request, visitor_id=None):
        """按游客查询轨迹"""
        queryset = self.get_queryset().filter(visitor_id=visitor_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SurveillancePointViewSet(viewsets.ModelViewSet):
    """监控点位ViewSet"""
    queryset = models.SurveillancePoint.objects.all().select_related('area')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area', 'device_status']

    def get_serializer_class(self):
        return serializers.SurveillancePointSerializer


class LawEnforcerViewSet(viewsets.ModelViewSet):
    """执法人员ViewSet"""
    queryset = models.LawEnforcer.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'enforcer_name']

    def get_serializer_class(self):
        return serializers.LawEnforcerSerializer


class SystemUserViewSet(viewsets.ModelViewSet):
    """系统用户管理ViewSet"""
    queryset = models.SystemUser.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role_type', 'account_status']
    search_fields = ['username', 'real_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SystemUserSerializer
        return serializers.SystemUserDetailSerializer


class FunctionalAreaViewSet(viewsets.ModelViewSet):
    """功能区域管理ViewSet"""
    queryset = models.FunctionalArea.objects.all()
    serializer_class = serializers.FunctionalAreaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area_type']
