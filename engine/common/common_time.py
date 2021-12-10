#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
"""
from datetime import datetime

from functools import wraps
import time


def get_max_time():
    return datetime.strptime("2100-01-01 01:01:01", "%Y-%m-%d %H:%M:%S")


def string_to_date(string):
    """
    #把字符串转成date
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d")


def string_to_datetime(string):
    """
    #把字符串转成datetime
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def date_to_time(timestring):
    """
    date转时间戳
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d'))


def datetime_to_time(timestring):
    """
    datetime转时间戳
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))


def get_system_datetime():
    """
    获取系统当前时间
    :return:
    """
    sys_time = time.time()
    result_time = int(sys_time * 1000)
    return result_time


def get_system_datetime_str():
    """
    获取系统当前时间
    :return:
    """
    str_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    return str_time


# 把时间戳转成字符串形式
def time_to_datetime(stamp):
    """
    时间戳转datetime
    :param stamp:
    :return:
    """
    time_stamp = int(stamp / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))


#####计算函数耗时装饰圈
def fun_time(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start_time = time.time()
        tempfun = func(*args, **kargs)
        end_time = time.time()
        real_time = end_time - start_time
        # print("function name=%s,args=%s,kargs=%s real time is %s" % (func.__name__, args, kargs, real_time))
        return tempfun

    return wrapper
