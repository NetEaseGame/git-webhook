# -*- coding: utf-8 -*-
'''
Created on 2015年8月24日

@author: hustcc
'''
import datetime
import time


# 当前时间，可用于mysql datetime
def now_datetime_string():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_datetime():
    return datetime.datetime.now()


def now_date_string():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def now_timestamp():
    return time.time()


if __name__ == '__main__':
    print now_datetime()
    print now_timestamp()
    print now_date_string()
