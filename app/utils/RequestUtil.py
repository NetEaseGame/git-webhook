# -*- coding: utf-8 -*-
'''
Created on 2015-8-21

@author: hustcc
'''

from flask.globals import request, session

# get / post data
def get_parameter(key, default=None):
    '''
    info:获得请求参数，包括get和post，其他类型的访问不管
    '''
    # post参数
    if request.method == 'POST':
        param = request.form.get(key, default)
    # get
    elif request.method == 'GET':
        param = request.args.get(key, default)
    else:
        return default

    return param


# login user from session
def get_login_user():
    return session.get('u_id', '')


# set user login
def login_user(user):
    session['u_id'] = user


# logou user, session pop
def logout():
    session.pop('u_id', '')
