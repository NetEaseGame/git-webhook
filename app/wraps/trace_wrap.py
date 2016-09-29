#coding=utf-8
'''
Created on 2015年8月21日

@author: hustcc
'''

from functools import wraps
import traceback

#定义一个trace监控的装饰器
def log_traceback(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #先执行方法，然后写日志
        try:
            func = f(*args, **kwargs)
            return func
        except:
            #如果出现trace异常，发送到服务器
            traceback.print_exc()
#             return func
            return "500"
    return decorated_function