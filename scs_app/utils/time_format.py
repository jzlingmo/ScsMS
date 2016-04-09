# -*- coding: utf-8 -*-

import time
import datetime


def now_timestamp():
    return int(time.time()*1000)

#把datetime转成字符串
def datetime_to_string(dt):
    return dt.strftime("%Y-%m-%d-%H")


#把字符串转成datetime
def string_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H")


#把字符串转成时间戳形式
def string_to_timestamp(strTime):
    return time.mktime(string_to_datetime(strTime).timetuple())


#把时间戳转成字符串形式
def timestamp_to_string(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))


#把datetime类型转外时间戳形式
def datetime_to_timestamp(dateTim):
    return time.mktime(dateTim.timetuple())