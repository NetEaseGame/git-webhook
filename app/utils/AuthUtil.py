# -*- coding: utf-8 -*-
'''
Created on 2016-11-11

@author: hustcc
'''
from app.database.model import WebHook, Collaborator
from sqlalchemy.sql.expression import false


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


def has_auth_webhooks(user_id):
    """获取所有我有权访问的Webhooks"""
    # create webhooks
    created_webhooks = WebHook.query.filter_by(
        user_id=user_id, deleted=False).all()

    # collaborator webhooks
    collaborated_webhooks = \
        WebHook.query.join(Collaborator,
                           Collaborator.webhook_id == WebHook.id) \
                     .filter(Collaborator.user_id == user_id) \
                     .filter(WebHook.deleted == false()).all()

    webhooks = created_webhooks + collaborated_webhooks
    # 去重并排序
    webhooks = list(sorted(set(webhooks), key=lambda x: x.id, reverse=True))
    return webhooks
