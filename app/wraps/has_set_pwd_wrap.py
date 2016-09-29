#coding=utf-8
'''
Created on 2015年8月21日

@author: hustcc
'''

from functools import wraps
from app.dbs import consts_dbs
from flask.globals import request
from flask.helpers import url_for
from werkzeug.utils import redirect
import urllib

def if_set_pwd():
    pwd = consts_dbs.get_password()
    if pwd and pwd.get('value', None):
        return True
    return False

#定义一个检查是否设置密码的装饰器，只有设置密码才能进一步使用
def has_set_pwd(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #查询数据库，看是否设置密码
        if if_set_pwd():
            #先执行方法，然后写日志
            func = f(*args, **kwargs)
            return func
        else:
            #跳转到配置密码页面
            return redirect(url_for('set_pwd', next = urllib.quote(request.url)))
    return decorated_function