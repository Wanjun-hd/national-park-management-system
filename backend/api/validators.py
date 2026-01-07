"""
数据验证器
Custom validators for National Park Management System
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_phone_number(value):
    """
    验证手机号码格式
    支持中国大陆11位手机号
    """
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            '请输入有效的手机号码（11位数字，以1开头）',
            params={'value': value},
        )


def validate_id_card(value):
    """
    验证身份证号码格式
    支持15位和18位身份证号
    """
    if len(value) not in [15, 18]:
        raise ValidationError('身份证号码必须是15位或18位')

    # 18位身份证号验证
    if len(value) == 18:
        pattern = r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
        if not re.match(pattern, value):
            raise ValidationError('身份证号码格式不正确')


def validate_email(value):
    """
    验证邮箱格式
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise ValidationError('请输入有效的邮箱地址')


def validate_positive_number(value):
    """
    验证正数
    """
    if value <= 0:
        raise ValidationError('数值必须大于0')


def validate_non_negative_number(value):
    """
    验证非负数
    """
    if value < 0:
        raise ValidationError('数值不能为负数')


def validate_percentage(value):
    """
    验证百分比（0-100）
    """
    if not 0 <= value <= 100:
        raise ValidationError('百分比必须在0到100之间')


def validate_latitude(value):
    """
    验证纬度（-90 到 90）
    """
    if not -90 <= value <= 90:
        raise ValidationError('纬度必须在-90到90之间')


def validate_longitude(value):
    """
    验证经度（-180 到 180）
    """
    if not -180 <= value <= 180:
        raise ValidationError('经度必须在-180到180之间')


def validate_future_date(value):
    """
    验证日期不能是过去的日期
    """
    if value < timezone.now().date():
        raise ValidationError('日期不能是过去的日期')


def validate_date_range(start_date, end_date):
    """
    验证日期范围（开始日期必须早于结束日期）
    """
    if start_date and end_date and start_date > end_date:
        raise ValidationError('开始日期必须早于结束日期')


def validate_capacity(current_count, max_capacity):
    """
    验证容量限制
    """
    if current_count > max_capacity:
        raise ValidationError(f'当前数量({current_count})不能超过最大容量({max_capacity})')


def validate_file_size(file, max_size_mb=10):
    """
    验证文件大小
    """
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'文件大小不能超过{max_size_mb}MB')


def validate_image_file(file):
    """
    验证图片文件类型
    """
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    file_ext = file.name.lower().split('.')[-1]

    if f'.{file_ext}' not in allowed_extensions:
        raise ValidationError('只支持JPG、PNG、GIF、WEBP格式的图片')


def validate_protection_level(value):
    """
    验证保护级别
    """
    valid_levels = ['国家一级保护', '国家二级保护', '省级保护', '市级保护', '无']
    if value not in valid_levels:
        raise ValidationError(f'保护级别必须是以下之一：{", ".join(valid_levels)}')


def validate_device_status(value):
    """
    验证设备状态
    """
    valid_statuses = ['正常', '故障', '维护中', '离线']
    if value not in valid_statuses:
        raise ValidationError(f'设备状态必须是以下之一：{", ".join(valid_statuses)}')


def validate_data_quality(value):
    """
    验证数据质量等级
    """
    valid_qualities = ['优秀', '良好', '合格', '异常']
    if value not in valid_qualities:
        raise ValidationError(f'数据质量必须是以下之一：{", ".join(valid_qualities)}')


def validate_username(value):
    """
    验证用户名格式
    只允许字母、数字、下划线，长度4-20
    """
    if not 4 <= len(value) <= 20:
        raise ValidationError('用户名长度必须在4到20个字符之间')

    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, value):
        raise ValidationError('用户名只能包含字母、数字和下划线')


def validate_password_strength(value):
    """
    验证密码强度
    至少8位，包含字母和数字
    """
    if len(value) < 8:
        raise ValidationError('密码长度至少为8位')

    if not re.search(r'[a-zA-Z]', value):
        raise ValidationError('密码必须包含字母')

    if not re.search(r'\d', value):
        raise ValidationError('密码必须包含数字')


def validate_latin_name(value):
    """
    验证拉丁学名格式
    基本格式：属名 + 种名
    """
    pattern = r'^[A-Z][a-z]+ [a-z]+( [a-z]+)?$'
    if not re.match(pattern, value):
        raise ValidationError('拉丁学名格式不正确，应为：属名（首字母大写） + 种名（小写）')


def validate_monitoring_value_range(value, indicator_name):
    """
    根据指标名称验证监测值范围
    """
    ranges = {
        '温度': (-50, 60),
        '湿度': (0, 100),
        'pH值': (0, 14),
        '溶解氧': (0, 20),
        '浊度': (0, 1000),
        'PM2.5': (0, 500),
        'PM10': (0, 1000),
        '负氧离子浓度': (0, 100000),
    }

    if indicator_name in ranges:
        min_val, max_val = ranges[indicator_name]
        if not min_val <= value <= max_val:
            raise ValidationError(f'{indicator_name}的值必须在{min_val}到{max_val}之间')


class ReservationValidator:
    """
    预约数据验证器
    """
    @staticmethod
    def validate_visitor_count(visitor_count):
        """验证游客数量"""
        if visitor_count <= 0:
            raise ValidationError('游客数量必须大于0')
        if visitor_count > 50:
            raise ValidationError('单次预约游客数量不能超过50人')

    @staticmethod
    def validate_reservation_date(reservation_date):
        """验证预约日期"""
        today = timezone.now().date()
        if reservation_date < today:
            raise ValidationError('预约日期不能是过去的日期')

        # 最多提前30天预约
        max_date = today + timezone.timedelta(days=30)
        if reservation_date > max_date:
            raise ValidationError('最多只能提前30天预约')

    @staticmethod
    def validate_payment_amount(amount, visitor_count):
        """验证支付金额"""
        # 假设单价为100元/人
        expected_amount = visitor_count * 100
        if abs(amount - expected_amount) > 0.01:
            raise ValidationError(f'支付金额不正确，应为{expected_amount}元')


class SpeciesValidator:
    """
    物种数据验证器
    """
    @staticmethod
    def validate_taxonomy(kingdom, phylum, class_name, order, family):
        """验证分类学层级的一致性"""
        # 这里可以添加更复杂的分类学验证逻辑
        if not all([kingdom, phylum, class_name, order, family]):
            raise ValidationError('分类学信息不完整')


class EnvironmentalDataValidator:
    """
    环境数据验证器
    """
    @staticmethod
    def validate_data_consistency(monitoring_value, data_quality):
        """验证数据值与质量等级的一致性"""
        # 如果数据质量为"异常"，需要有合理的说明
        if data_quality == '异常' and monitoring_value is None:
            raise ValidationError('异常数据必须提供监测值')
