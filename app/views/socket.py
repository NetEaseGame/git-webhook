# -*- coding: utf-8 -*-
'''
Created on 2016年11月17日

@author: hustcc
'''
from app import socketio
from app.utils import AuthUtil, RequestUtil
import flask_socketio


@socketio.on('connect')
def on_socketio_connect():
    # 连接时自动监听所有有权限的 webhook
    user_id = RequestUtil.get_login_user().get('id', '')
    # 未登录，拒绝连接
    if not user_id:
        return False
    webhooks = AuthUtil.has_auth_webhooks(user_id)
    for webhook in webhooks:
        flask_socketio.join_room(webhook.id)
