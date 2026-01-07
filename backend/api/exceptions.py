"""
自定义异常处理器
Custom exception handlers for National Park Management System
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    统一处理所有异常并返回标准格式的响应
    """
    # 调用DRF的默认异常处理器
    response = exception_handler(exc, context)

    # 如果DRF已经处理了异常，直接返回
    if response is not None:
        # 统一响应格式
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': get_error_message(exc),
                'details': response.data
            }
        }
        response.data = custom_response_data
        return response

    # 处理Django的ValidationError
    if isinstance(exc, DjangoValidationError):
        logger.warning(f'Validation error: {str(exc)}')
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': '数据验证失败',
                'details': exc.messages if hasattr(exc, 'messages') else str(exc)
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    # 处理数据库错误
    if isinstance(exc, DatabaseError):
        logger.error(f'Database error: {str(exc)}')
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': '数据库操作失败',
                'details': '服务器内部错误，请稍后重试' if not settings.DEBUG else str(exc)
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 处理其他未捕获的异常
    logger.error(f'Unhandled exception: {type(exc).__name__}: {str(exc)}', exc_info=True)
    return Response({
        'success': False,
        'error': {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': '服务器内部错误',
            'details': str(exc) if settings.DEBUG else '请联系管理员'
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_error_message(exc):
    """
    根据异常类型获取友好的错误消息
    """
    error_messages = {
        'NotAuthenticated': '未认证，请先登录',
        'AuthenticationFailed': '认证失败，请检查登录凭证',
        'PermissionDenied': '权限不足，无法执行该操作',
        'NotFound': '请求的资源不存在',
        'MethodNotAllowed': '不支持该请求方法',
        'ValidationError': '数据验证失败',
        'ParseError': '请求数据格式错误',
        'Throttled': '请求过于频繁，请稍后重试',
    }

    exc_class_name = exc.__class__.__name__
    return error_messages.get(exc_class_name, '请求处理失败')


# 自定义业务异常类
class BusinessException(Exception):
    """
    业务逻辑异常基类
    """
    def __init__(self, message, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code or status_code
        self.status_code = status_code
        super().__init__(message)


class SpeciesNotFoundException(BusinessException):
    """物种不存在异常"""
    def __init__(self, species_id):
        super().__init__(
            message=f'物种(ID: {species_id})不存在',
            code='SPECIES_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND
        )


class HabitatNotFoundException(BusinessException):
    """栖息地不存在异常"""
    def __init__(self, habitat_id):
        super().__init__(
            message=f'栖息地(ID: {habitat_id})不存在',
            code='HABITAT_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND
        )


class DeviceOfflineException(BusinessException):
    """设备离线异常"""
    def __init__(self, device_id):
        super().__init__(
            message=f'设备(ID: {device_id})已离线，无法进行操作',
            code='DEVICE_OFFLINE',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ReservationFullException(BusinessException):
    """预约已满异常"""
    def __init__(self, date):
        super().__init__(
            message=f'{date}的预约名额已满',
            code='RESERVATION_FULL',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ReservationCancelledException(BusinessException):
    """预约已取消异常"""
    def __init__(self, reservation_id):
        super().__init__(
            message=f'预约(ID: {reservation_id})已被取消',
            code='RESERVATION_CANCELLED',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class CapacityExceededException(BusinessException):
    """容量超限异常"""
    def __init__(self, area_name, current, max_capacity):
        super().__init__(
            message=f'{area_name}的游客数量({current})已达到最大容量({max_capacity})',
            code='CAPACITY_EXCEEDED',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class IllegalBehaviorAlreadyHandledException(BusinessException):
    """违法行为已处理异常"""
    def __init__(self, behavior_id):
        super().__init__(
            message=f'违法行为(ID: {behavior_id})已经处理完成，无法再次处理',
            code='ILLEGAL_BEHAVIOR_ALREADY_HANDLED',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ProjectNotFoundException(BusinessException):
    """科研项目不存在异常"""
    def __init__(self, project_id):
        super().__init__(
            message=f'科研项目(ID: {project_id})不存在',
            code='PROJECT_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND
        )


class ProjectClosedException(BusinessException):
    """项目已结题异常"""
    def __init__(self, project_id):
        super().__init__(
            message=f'科研项目(ID: {project_id})已结题，无法继续添加数据',
            code='PROJECT_CLOSED',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class DataAccessDeniedException(BusinessException):
    """数据访问被拒绝异常"""
    def __init__(self, resource_type):
        super().__init__(
            message=f'您没有权限访问该{resource_type}',
            code='DATA_ACCESS_DENIED',
            status_code=status.HTTP_403_FORBIDDEN
        )


class InvalidDateRangeException(BusinessException):
    """无效日期范围异常"""
    def __init__(self):
        super().__init__(
            message='开始日期必须早于结束日期',
            code='INVALID_DATE_RANGE',
            status_code=status.HTTP_400_BAD_REQUEST
        )


class AccountLockedException(BusinessException):
    """账号被锁定异常"""
    def __init__(self, username):
        super().__init__(
            message=f'账号({username})已被锁定，请联系管理员',
            code='ACCOUNT_LOCKED',
            status_code=status.HTTP_403_FORBIDDEN
        )


class AccountDisabledException(BusinessException):
    """账号已停用异常"""
    def __init__(self, username):
        super().__init__(
            message=f'账号({username})已被停用',
            code='ACCOUNT_DISABLED',
            status_code=status.HTTP_403_FORBIDDEN
        )


class InvalidPasswordException(BusinessException):
    """密码错误异常"""
    def __init__(self, remaining_attempts):
        super().__init__(
            message=f'密码错误，还有{remaining_attempts}次机会',
            code='INVALID_PASSWORD',
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class DuplicateDataException(BusinessException):
    """数据重复异常"""
    def __init__(self, field_name, value):
        super().__init__(
            message=f'{field_name}({value})已存在',
            code='DUPLICATE_DATA',
            status_code=status.HTTP_400_BAD_REQUEST
        )


# 导入settings用于DEBUG模式判断
from django.conf import settings
