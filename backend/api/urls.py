"""
API URL Configuration
完整的API路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()

# 生物多样性监测
router.register(r'biodiversity/species', views.SpeciesViewSet, basename='species')
router.register(r'biodiversity/habitats', views.HabitatViewSet, basename='habitat')
router.register(r'biodiversity/devices', views.MonitoringDeviceViewSet, basename='monitoring-device')
router.register(r'biodiversity/monitoring-records', views.MonitoringRecordViewSet, basename='monitoring-record')

# 环境监测
router.register(r'environment/indicators', views.MonitoringIndicatorViewSet, basename='indicator')
router.register(r'environment/data', views.EnvironmentalDataViewSet, basename='environmental-data')
router.register(r'environment/devices', views.MonitoringDeviceViewSet, basename='env-device')

# 游客管理
router.register(r'visitor/visitors', views.VisitorViewSet, basename='visitor')
router.register(r'visitor/reservations', views.ReservationViewSet, basename='reservation')
router.register(r'visitor/traffic-controls', views.TrafficControlViewSet, basename='traffic-control')
router.register(r'visitor/trajectories', views.VisitorTrajectoryViewSet, basename='visitor-trajectory')

# 执法监管
router.register(r'enforcement/illegal-behaviors', views.IllegalBehaviorViewSet, basename='illegal-behavior')
router.register(r'enforcement/dispatches', views.EnforcementDispatchViewSet, basename='dispatch')
router.register(r'enforcement/surveillance-points', views.SurveillancePointViewSet, basename='surveillance-point')
router.register(r'enforcement/enforcers', views.LawEnforcerViewSet, basename='law-enforcer')

# 科研支撑
router.register(r'research/projects', views.ResearchProjectViewSet, basename='research-project')
router.register(r'research/data-collections', views.ResearchDataCollectionViewSet, basename='data-collection')
router.register(r'research/achievements', views.ResearchAchievementViewSet, basename='achievement')

# 系统管理
router.register(r'system/users', views.SystemUserViewSet, basename='system-user')
router.register(r'system/areas', views.FunctionalAreaViewSet, basename='functional-area')

# URL模式
urlpatterns = [
    # 认证相关
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/current-user/', views.current_user_view, name='current-user'),
    path('auth/create-test-user/', views.create_test_user, name='create-test-user'),

    # 统计分析
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('biodiversity/stats/', views.biodiversity_stats, name='biodiversity-stats'),
    path('visitor/stats/', views.visitor_stats, name='visitor-stats'),
    path('enforcement/stats/', views.enforcement_stats, name='enforcement-stats'),
    path('research/stats/', views.research_stats, name='research-stats'),

    # 测试API
    path('test/', views.test_api, name='test-api'),
]

# 将路由器的URL添加到urlpatterns
urlpatterns += router.urls
