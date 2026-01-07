"""
工具函数
Utility functions for National Park Management System
"""
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import hashlib
import random
import string


def generate_id(prefix, length=6):
    """
    生成唯一ID
    例如: generate_id('S', 6) -> 'S000001'
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(random.choices(string.digits, k=length))
    return f"{prefix}{timestamp[-length:]}{random_suffix[-2:]}"


def hash_password(password):
    """
    使用SHA-256加密密码
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, password_hash):
    """
    验证密码
    """
    return hash_password(password) == password_hash


def get_date_range(range_type='today'):
    """
    获取日期范围
    支持: today, week, month, year
    """
    today = timezone.now().date()
    ranges = {
        'today': (today, today),
        'week': (today - timedelta(days=7), today),
        'month': (today - timedelta(days=30), today),
        'year': (today - timedelta(days=365), today),
    }
    return ranges.get(range_type, (today, today))


def calculate_age(birth_date):
    """
    根据出生日期计算年龄
    """
    today = timezone.now().date()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age


def format_file_size(size_bytes):
    """
    格式化文件大小
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def build_search_query(fields, search_term):
    """
    构建搜索查询
    支持多字段模糊搜索
    """
    query = Q()
    for field in fields:
        query |= Q(**{f'{field}__icontains': search_term})
    return query


def paginate_queryset(queryset, page, page_size=20):
    """
    手动分页
    """
    start = (page - 1) * page_size
    end = start + page_size
    total = queryset.count()
    items = queryset[start:end]

    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'items': items
    }


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    计算两点之间的距离（单位：千米）
    使用Haversine公式
    """
    from math import radians, cos, sin, asin, sqrt

    # 将十进制度数转化为弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为千米
    return c * r


def get_season(date=None):
    """
    获取季节
    """
    if date is None:
        date = timezone.now().date()

    month = date.month
    if 3 <= month <= 5:
        return '春季'
    elif 6 <= month <= 8:
        return '夏季'
    elif 9 <= month <= 11:
        return '秋季'
    else:
        return '冬季'


def calculate_percentage(part, total):
    """
    计算百分比
    """
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def get_time_of_day():
    """
    获取时段
    """
    hour = timezone.now().hour
    if 5 <= hour < 8:
        return '清晨'
    elif 8 <= hour < 12:
        return '上午'
    elif 12 <= hour < 14:
        return '中午'
    elif 14 <= hour < 18:
        return '下午'
    elif 18 <= hour < 22:
        return '晚上'
    else:
        return '深夜'


def mask_sensitive_data(data, mask_char='*', visible_chars=4):
    """
    遮蔽敏感数据
    例如: mask_sensitive_data('13812345678') -> '138****5678'
    """
    if not data or len(data) <= visible_chars:
        return data

    masked_length = len(data) - visible_chars
    return data[:visible_chars//2] + mask_char * masked_length + data[-visible_chars//2:]


def mask_phone(phone):
    """
    遮蔽手机号中间4位
    """
    if len(phone) == 11:
        return phone[:3] + '****' + phone[7:]
    return phone


def mask_id_card(id_card):
    """
    遮蔽身份证号中间10位
    """
    if len(id_card) == 18:
        return id_card[:4] + '**********' + id_card[14:]
    return id_card


class DataExporter:
    """
    数据导出工具类
    支持CSV、JSON等格式
    """

    @staticmethod
    def to_csv(queryset, fields, filename='export.csv'):
        """
        导出为CSV格式
        """
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # 写入表头
        writer.writerow(fields)

        # 写入数据
        for obj in queryset:
            row = [getattr(obj, field, '') for field in fields]
            writer.writerow(row)

        return output.getvalue()

    @staticmethod
    def to_json(queryset, serializer_class):
        """
        导出为JSON格式
        """
        from rest_framework.renderers import JSONRenderer

        serializer = serializer_class(queryset, many=True)
        return JSONRenderer().render(serializer.data)


class DateRangeFilter:
    """
    日期范围过滤器
    """

    @staticmethod
    def filter_by_date_range(queryset, date_field, start_date, end_date):
        """
        按日期范围过滤
        """
        filters = {}
        if start_date:
            filters[f'{date_field}__gte'] = start_date
        if end_date:
            filters[f'{date_field}__lte'] = end_date
        return queryset.filter(**filters)

    @staticmethod
    def filter_by_recent_days(queryset, date_field, days=7):
        """
        过滤最近N天的数据
        """
        start_date = timezone.now().date() - timedelta(days=days)
        return queryset.filter(**{f'{date_field}__gte': start_date})


class StatisticsHelper:
    """
    统计分析辅助类
    """

    @staticmethod
    def calculate_growth_rate(current, previous):
        """
        计算增长率
        """
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)

    @staticmethod
    def calculate_average(values):
        """
        计算平均值
        """
        if not values:
            return 0
        return sum(values) / len(values)

    @staticmethod
    def calculate_trend(values):
        """
        计算趋势（上升、下降、平稳）
        """
        if len(values) < 2:
            return '平稳'

        recent = values[-3:] if len(values) >= 3 else values
        if all(recent[i] <= recent[i+1] for i in range(len(recent)-1)):
            return '上升'
        elif all(recent[i] >= recent[i+1] for i in range(len(recent)-1)):
            return '下降'
        else:
            return '波动'


def generate_report_filename(report_type, extension='pdf'):
    """
    生成报告文件名
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{report_type}_report_{timestamp}.{extension}"


def validate_business_hours(time_value, start_hour=8, end_hour=18):
    """
    验证是否在营业时间内
    """
    hour = time_value.hour if isinstance(time_value, datetime) else time_value
    return start_hour <= hour < end_hour


def format_duration(seconds):
    """
    格式化时长
    例如: format_duration(3661) -> '1小时1分1秒'
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f'{hours}小时')
    if minutes > 0:
        parts.append(f'{minutes}分')
    if secs > 0 or not parts:
        parts.append(f'{secs}秒')

    return ''.join(parts)
