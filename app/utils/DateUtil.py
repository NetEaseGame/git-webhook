#coding=utf-8
'''
Created on 2015年8月24日

@author: hustcc
'''
import datetime


#当前时间，可用于mysql datetime
def now_datetime():
    return datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print now_datetime()