#!/usr/bin/python
# -*- coding: UTF-8 -*

from datetime import datetime

from functools import wraps
import time


def get_max_time():
    return datetime.strptime("2100-01-01 01:01:01", "%Y-%m-%d %H:%M:%S")


def string_to_date(string):
    """
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d")


def string_to_datetime(string):
    """
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def date_to_time(timestring):
    """
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d'))


def datetime_to_time(timestring):
    """
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))


def get_system_datetime():
    """
    :return:
    """
    sys_time = time.time()
    result_time = int(sys_time * 1000)
    return result_time


def get_system_datetime_str():
    """
    :return:
    """
    str_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    return str_time


def time_to_datetime(stamp):
    """
    :param stamp:
    :return:
    """
    time_stamp = int(stamp / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))

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
