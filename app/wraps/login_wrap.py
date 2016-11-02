# -*- coding: utf-8 -*-
'''
Created on 2015年1月28日

@author: hustcc
'''
from functools import wraps

from flask import request, redirect, url_for

from app.utils import RequestUtil, JsonUtil


# type should be in ['page','api]
def login_required(type='api'):
    '''need login wrap'''
    def _login_required(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not RequestUtil.get_login_user():
                if type == 'page':
                    return redirect(url_for('login', next=request.url))
                else:
                    return JsonUtil.object_2_json({
                        'success': 0,
                        'data': 'the interface need to be login'
                    })
            return function(*args, **kwargs)

        return decorated_function

    return _login_required
