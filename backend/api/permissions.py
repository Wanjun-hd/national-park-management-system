"""
自定义权限类
Role-based access control for National Park Management System
"""
from rest_framework import permissions


class IsSystemAdmin(permissions.BasePermission):
    """
    系统管理员权限
    只允许系统管理员访问
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request, 'user'):
            return False
        # 从JWT token中获取角色
        return getattr(request.user, 'role_type', None) == '系统管理员'


class IsEcologyMonitor(permissions.BasePermission):
    """
    生态监测员权限
    允许生态监测员和管理员访问
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request, 'user'):
            return False
        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '生态监测员']


class IsEnvironmentMonitor(permissions.BasePermission):
    """
    环境监测员权限
    允许环境监测员和管理员访问
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request, 'user'):
            return False
        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '环境监测员']


class IsVisitorManager(permissions.BasePermission):
    """
    游客管理员权限
    允许游客管理员和管理员访问
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request, 'user'):
            return False
        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '游客管理员']


class IsEnforcementOfficer(permissions.BasePermission):
    """
    执法人员权限
    允许执法人员和管理员访问
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request, 'user'):
            return False
        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '执法人员']


class IsResearcher(permissions.BasePermission):
    """
    科研人员权限
    允许科研人员和管理员访问
    """
    def has_permission(self, request, view):
        if not request.user or not hasattr(request, 'user'):
            return False
        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '科研人员']


class IsReadOnlyOrAdmin(permissions.BasePermission):
    """
    只读或管理员权限
    允许所有用户读取，只允许管理员修改
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not hasattr(request, 'user'):
            return False

        return getattr(request.user, 'role_type', None) == '系统管理员'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    所有者或管理员权限
    允许对象的创建者或管理员访问
    """
    def has_object_permission(self, request, view, obj):
        # 管理员拥有所有权限
        if getattr(request.user, 'role_type', None) == '系统管理员':
            return True

        # 检查对象是否有 creator/recorder/collector 等字段
        if hasattr(obj, 'recorder'):
            return obj.recorder == request.user
        elif hasattr(obj, 'collector'):
            return obj.collector == request.user
        elif hasattr(obj, 'enforcer'):
            return obj.enforcer == request.user
        elif hasattr(obj, 'principal'):
            return obj.principal == request.user

        return False


class CanModifyProtectedSpecies(permissions.BasePermission):
    """
    保护物种修改权限
    只允许系统管理员和生态监测员修改保护级别高的物种
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not hasattr(obj, 'protection_level'):
            return True

        if obj.protection_level in ['国家一级保护', '国家二级保护']:
            role = getattr(request.user, 'role_type', None)
            return role in ['系统管理员', '生态监测员']

        return True


class CanApproveReservation(permissions.BasePermission):
    """
    预约审批权限
    只允许游客管理员和系统管理员审批预约
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '游客管理员']


class CanHandleIllegalBehavior(permissions.BasePermission):
    """
    违法行为处理权限
    只允许执法人员和系统管理员处理违法行为
    """
    def has_permission(self, request, view):
        role = getattr(request.user, 'role_type', None)
        return role in ['系统管理员', '执法人员']


class CanAccessResearchData(permissions.BasePermission):
    """
    科研数据访问权限
    根据数据共享权限决定访问
    """
    def has_object_permission(self, request, view, obj):
        # 管理员和数据创建者可以访问所有数据
        role = getattr(request.user, 'role_type', None)
        if role == '系统管理员':
            return True

        if hasattr(obj, 'collector') and obj.collector == request.user:
            return True

        # 检查项目成果的共享权限
        if hasattr(obj, 'share_permission'):
            if obj.share_permission == '公开':
                return True
            elif obj.share_permission == '内部共享':
                return role in ['科研人员', '生态监测员', '环境监测员']
            elif obj.share_permission == '保密':
                return False

        return False
