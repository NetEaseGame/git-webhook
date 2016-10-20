# -*- coding: utf-8 -*-
'''
Created on 2016-2-19

@author: hzwangzhiwei
'''
from app.utils import JsonUtil
import flask
from app.utils import RequestUtil


def standard_response(success, data):
    '''standard response
    '''
    rst = {}
    rst['success'] = success
    rst['data'] = data
    return JsonUtil.object_2_json(rst)


# 重写 render_template 写入固定的一些参数
def render_template(*args, **kwargs):
    kwargs['loginUser'] = JsonUtil.object_2_json(RequestUtil.get_login_user())
    return flask.render_template(*args, **kwargs)
