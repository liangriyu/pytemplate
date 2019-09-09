# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 10:47
# @Author  : liangriyu

#时间格式
from datetime import datetime,timedelta

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT2 = "%Y%m%d%H%M%S"
DATETIME_FORMAT_D = "%Y-%m-%d"
DATETIME_FORMAT_D2 = "%Y%m%d"
DATETIME_FORMAT_H = "%Y-%m-%d %H"
DATETIME_FORMAT_H2 = "%Y%m%d%H"
DATETIME_FORMAT_M = "%Y-%m-%d %H:%M"
DATETIME_FORMAT_M2 = "%Y%m%d%H%M%S"
DATETIME_FORMAT_MS = "%Y-%m-%d %H:%M:%S.%f"
DATETIME_FORMAT_MS2 = "%Y%m%d%H%M%S%f"

def format2dtime(str_dtime,format):
    return datetime.strptime(str_dtime,format)

def format2str(dtime,format):
    return dtime.strftime(format)

def add_timedelta(dtime,days=0,hours=0,minutes=0,seconds=0):
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
        dtime = format2dtime(dtime,format)
    dtime = dtime + timedelta(days=days)
    dtime = dtime + timedelta(hours=hours)
    dtime = dtime + timedelta(minutes=minutes)
    dtime = dtime + timedelta(seconds=seconds)
    return dtime


