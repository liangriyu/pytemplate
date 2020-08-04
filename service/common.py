import json
import traceback
import uuid
import decimal

from datetime import datetime, date, timedelta

from xlrd import xldate_as_datetime
from xlrd import xldate_as_tuple

from hdcloud.base.excepts import ValidateException
from hdcloud.utils import dateutil

def reduce_dt(strdate, strsub):
    if str(strsub) == "24:00":
        strsub = "23:45"
        dt = dateutil.format2dtime(strdate + " " + strsub, dateutil.DATE_FORMAT_M)
    else:
        dt = dateutil.format2dtime(strdate + " " + strsub, dateutil.DATE_FORMAT_M)
        dt = dateutil.add_timedelta(dt, 0, 0, -15, 0)
    return dateutil.format2str(dt, dateutil.DATE_FORMAT_M2)

def time_list():
    time_list=[]
    for hour in range(0, 25):
        for minute in range(0, 4):
            if hour == 0 and minute == 0:
                continue
            if hour == 24 and minute > 0:
                break
            time_list.append(str(hour).zfill(2) + ":" + str(minute * 15).zfill(2))
    return time_list


def trim_file_name(file_name):
    last_char = file_name[-1:]
    if '"' == last_char :
        return file_name[:-1]
    return file_name


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def safe_int(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        val = val.strip()
    try:
        if isinstance(val, str) and "." in val:
            return int(float(val))
        return int(val)
    except Exception:
        raise ValidateException( 'safe_int error ,'
                                                     'val:{0}'.format(val))


def safe_float(val):
    if isinstance(val, float):
        return val
    if isinstance(val, int):
        return float(val)
    if isinstance(val, str):
        val = val.strip()
    try:
        return float(val)
    except Exception:
        raise ValidateException( 'safe_float error ,'
                                                     'val:{0}'.format(val))


def safe_str(val, encodeing="utf-8"):
    try:
        if not isinstance(val, str):
            return str(val)
        if isinstance(val, bytes):
            return val.encode(encodeing, "replace")
        return val
    except Exception:
        raise ValidateException( 'safe_str error ,'
                                                     'val:{0}'.format(val))


def trans_str_date_format(cvalue, ctype):
    try:
        # ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        # ctype =3,为日期
        if ctype == 3:
            date = datetime(*xldate_as_tuple(cvalue, 0))
            return date.strftime('%Y-%m-%d')  # ('%Y/%m/%d %H:%M:%S')
        # ctype =1，为字符串
        elif ctype == 1:
            if dateutil.vaild_date(cvalue):
                t1 = datetime.strptime(cvalue, "%Y-%m-%d")
                return dateutil.format2str(t1, "yyyy-mm-dd")
        return None
    except:
        return None

def trans_str_time_format(cvalue, ctype):
    try:
        # ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        # ctype =3,为日期
        if ctype == 3:
            date = dateutil.format2dtime("2020-01-01 00:00:00")
            try:
                dt = xldate_as_datetime(cvalue, 0)
            except:
                # print(traceback.format_exc())
                t = xldate_as_tuple(cvalue, 0)
                dt = date+timedelta(hours=t[3],minutes=t[4],seconds=t[5])
            return dt.strftime('%H:%M:%S')
        # ctype =1，为字符串
        elif ctype == 1:
            if str(cvalue).endswith("24:00") or str(cvalue).endswith("24:00:00"):
                cvalue="00:00"
            if dateutil.vaild_date(cvalue):
                t1 = datetime.strptime(cvalue, "%H:%M:%S")
                return dateutil.format2str(t1, "%H:%M:%S")
            else:
                if len(cvalue)==5:
                    t1 = datetime.strptime(cvalue, "%H:%M")
                else:
                    t1 = datetime.strptime(cvalue, "%H:%M:%S")
                return dateutil.format2str(t1, "%H:%M:%S")
        return None
    except:
        # print(traceback.format_exc())
        return None

def timedelta2date(y,m,d,h,i,s):
    return timedelta(hours=h,minutes=i,seconds=s)