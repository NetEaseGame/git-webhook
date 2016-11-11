# -*- coding: utf-8 -*-
'''
Created on 2016-11-11

@author: hustcc
'''
from app.database.model import WebHook, Collaborator


# 具有只读权限
def has_readonly_auth(user_id, webhook_id):
    return has_admin_auth(user_id, webhook_id) or \
           has_collaborator_auth(user_id, webhook_id)


# 是否有创建者权限
def has_admin_auth(user_id, webhook_id):
    return WebHook.query.filter_by(user_id=user_id,
                                   id=webhook_id).first()


# 是否有观察者权限
def has_collaborator_auth(user_id, webhook_id):
    return Collaborator.query.filter_by(user_id=user_id,
                                        webhook_id=webhook_id).first()
