"""
时间处理工具
"""
import datetime

FORMAT_DATE = '%Y-%m-%d'
FORMAT_DATE2 = '%Y%m%d'
FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'


def get_now_str(date_format=FORMAT_DATETIME):
    """
    获取当前时间的字符串
    :param date_format:
    :return:
    """
    return datetime_to_str(datetime.datetime.now(), date_format=date_format)


def timestamp_to_datetime(timestamp: int):
    """
    时间戳转datetime
    :param timestamp:
    :return:
    """
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp_to_str(timestamp: int, date_format: str = FORMAT_DATE, process_none: bool = False):
    """
    时间戳转时间字符串
    165656565-》‘2020-12-12’
    :param timestamp:
    :param date_format:
    :param process_none:
    :return:
    """
    return datetime_to_str(timestamp_to_datetime(timestamp), date_format=date_format, process_none=process_none)


def datetime_to_str(dt: datetime.datetime, date_format: str = FORMAT_DATE, process_none: bool = False):
    """
    datetime转时间字符串
    :param dt:
    :param date_format:
    :param process_none:
    :return:
    """
    if process_none and dt is None:
        return ''
    return dt.strftime(date_format)


def str_to_datetime(date_str: str, date_format: str = FORMAT_DATE, process_none: bool = False):
    """
    字符串转datetime
    :param date_str:
    :param date_format:
    :param process_none:
    :return:
    """
    if process_none and not date_str:
        return None
    return datetime.datetime.strptime(date_str, date_format)
