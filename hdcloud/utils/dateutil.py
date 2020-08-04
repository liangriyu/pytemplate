# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 10:47
# @Author  : liangriyu

# 时间格式
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT2 = "%Y%m%d%H%M%S"
DATE_FORMAT_D = "%Y-%m-%d"
DATE_FORMAT_D2 = "%Y%m%d"
DATE_FORMAT_H = "%Y-%m-%d %H"
DATE_FORMAT_H2 = "%Y%m%d%H"
DATE_FORMAT_M = "%Y-%m-%d %H:%M"
DATE_FORMAT_M2 = "%Y%m%d%H%M"
DATE_FORMAT_MS = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT_MS2 = "%Y%m%d%H%M%S%f"


def format2dtime(str_dtime, format=DATE_FORMAT):
    return datetime.strptime(str_dtime, format)


def format2str(dtime, format=DATE_FORMAT):
    return dtime.strftime(format)


def datestr_format(sdate, format=DATE_FORMAT):
    if ":" in sdate:
        dt = datetime.strptime(sdate, DATE_FORMAT)
    else:
        dt = datetime.strptime(sdate, DATE_FORMAT_D)
    return dt.strftime(format)


def add_timedelta(dtime, days=0, hours=0, minutes=0, seconds=0):
    """
    日期时间偏移
    :param dtime: 日期时间
    :param days: 偏移天数
    :param hours: 偏移小时数
    :param minutes: 偏移分钟数
    :param seconds: 偏移秒数
    :return:
    """
    if not isinstance(dtime, datetime):
        dtime = format2dtime(dtime, format)
    dtime = dtime + timedelta(days=days)
    dtime = dtime + timedelta(hours=hours)
    dtime = dtime + timedelta(minutes=minutes)
    dtime = dtime + timedelta(seconds=seconds)
    return dtime


def vaild_date(date):
    try:
        if "/" in date and ":" in date:
            datetime.strptime(date, "%Y/%m/%d %H:%M:%S")
        elif "/" in date:
            datetime.strptime(date, "%Y/%m/%d")
        elif ":" in date:
            datetime.strptime(date, DATE_FORMAT)
        else:
            datetime.strptime(date, DATE_FORMAT_D)
        return 1
    except Exception as e:
        return 0


def get_current_time_str(format=DATE_FORMAT):
    """
    获取当前时间字符串
    :param format:
    :return:
    """
    return format2str(datetime.now(), format)

def get_time_list_str(star_time, end_time, step=1, step_type='days',date_format = "%Y-%m-%d %H:%M:%S"):
    """
    获取开始结束时间范围时间列表
    :param star_time:开始时间
    :param end_time:结束时间
    :param step:间隔步长
    :param step_type:间隔步长类型 日时分秒周
    :return:
    """
    yield star_time
    if step_type== 'hours':
        td = timedelta(hours=step)
    elif step_type== 'minutes':
        td = timedelta(minutes=step)
    elif step_type == 'seconds':
        td = timedelta(seconds=step)
    elif step_type == 'weeks':
        td = timedelta(weeks=step)
    else:
        td = timedelta(days=step)
    while star_time < end_time:
        start = datetime.strptime(star_time, date_format) + td
        star_time = datetime.strftime(start, date_format)
        yield star_time
