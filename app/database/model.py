# -*- coding: utf-8 -*-
'''
Created on 2016年6月15日

@author: hustcc
'''
import datetime
from app import SQLAlchemyDB as db, socketio
from app.database.base import BaseMethod
from app.utils import JsonUtil
from sqlalchemy.sql.expression import false


class User(db.Model, BaseMethod):
    '''user'''
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32))
    location = db.Column(db.String(32))
    avatar = db.Column(db.String(128))

    src = db.Column(db.String(4), default="gh")  # useless
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)

    def dict(self):
        rst = {}
        rst['id'] = self.id
        rst['name'] = self.name
        rst['location'] = self.location
        rst['avatar'] = self.avatar
        rst['src'] = self.src
        rst['last_login'] = self.last_login
        return rst


class Server(db.Model, BaseMethod):
    '''server list'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ip = db.Column(db.String(16))
    port = db.Column(db.Integer)
    account = db.Column(db.String(32))
    pkey = db.Column(db.Text)

    user_id = db.Column(db.String(32), db.ForeignKey(User.id))
    user = db.relationship(User)

    add_time = db.Column(db.DateTime, default=datetime.datetime.now)

    deleted = db.Column(db.Boolean, default=False)

    def dict(self, with_pkey=False):
        rst = {}
        rst['id'] = self.id
        rst['name'] = self.name
        rst['ip'] = self.ip
        rst['port'] = self.port
        rst['account'] = self.account
        rst['pkey'] = with_pkey and self.pkey or ''
        rst['user_id'] = self.user_id
        rst['add_time'] = self.add_time
        return rst


class WebHook(db.Model, BaseMethod):
    '''webhook'''
    id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(32))  # repo name
    branch = db.Column(db.String(32))  # repo branch
    shell = db.Column(db.Text)  # do what

    user_id = db.Column(db.String(32), db.ForeignKey(User.id))
    user = db.relationship(User)

    server_id = db.Column(db.Integer, db.ForeignKey(Server.id))
    server = db.relationship(Server)

    add_time = db.Column(db.DateTime, default=datetime.datetime.now)

    deleted = db.Column(db.Boolean, default=False)

    key = db.Column(db.String(32), unique=True)  # 用于webhook，保证私密，直接用 md5 salt

    # 1:waiting, 2:ing, 3:error, 4:success, 5:except, other
    status = db.Column(db.String(1))
    lastUpdate = db.Column(
        db.DateTime, default=datetime.datetime.now)  # 最新执行时间

    def dict(self, with_key=False):
        rst = {}
        rst['id'] = self.id
        rst['repo'] = self.repo
        rst['branch'] = self.branch
        rst['shell'] = self.shell
        rst['user_id'] = self.user_id
        rst['server_id'] = self.server_id
        rst['server'] = self.server and self.server.dict() or {}
        rst['add_time'] = self.add_time
        rst['key'] = with_key and self.key or ''
        rst['status'] = self.status
        rst['lastUpdate'] = self.lastUpdate
        return rst

    def updateStatus(self, status):
        self.status = status
        self.lastUpdate = datetime.datetime.now()
        self.save()
        data = JsonUtil.object_2_json(self.dict())
        socketio.emit('webhook', data, room=self.id)


def my_webhooks(user_id):
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
    webhooks = sorted(set(webhooks), key=lambda x: x.id, reverse=True)
    return list(webhooks)


class History(db.Model, BaseMethod):
    '''push history'''
    # md5, notice, output, push_name, push_email, success, add_time
    id = db.Column(db.Integer, primary_key=True)
    # 1:waiting, 2:ing, 3:error, 4:success, 5:except, other
    status = db.Column(db.String(1))
    shell_log = db.Column(db.Text)  # hook shell log

    data = db.Column(db.Text)  # git push data
    push_user = db.Column(db.String(64))  # git push user(name<email>)
    add_time = db.Column(
        db.DateTime, default=datetime.datetime.now)  # git push time
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now)  # last update time
    webhook_id = db.Column(db.Integer, db.ForeignKey(WebHook.id))
    webhook = db.relationship(WebHook)

    def dict(self):
        rst = {}
        rst['id'] = self.id
        rst['status'] = self.status
        rst['shell_log'] = self.shell_log
        rst['data'] = self.data  # json
        rst['push_user'] = self.push_user
        rst['add_time'] = self.add_time
        rst['update_time'] = self.update_time
        rst['webhook_id'] = self.webhook_id
        return rst

    def updateStatus(self, status):
        self.update_time = datetime.datetime.now()
        self.status = status
        self.save()
        data = JsonUtil.object_2_json(self.dict())
        socketio.emit('history', data, room=self.webhook.id)


class Collaborator(db.Model, BaseMethod):
    '''Collaborator'''
    id = db.Column(db.Integer, primary_key=True)
    # webhook
    webhook_id = db.Column(db.Integer, db.ForeignKey(WebHook.id))
    webhook = db.relationship(WebHook)
    # user
    user_id = db.Column(db.String(32), db.ForeignKey(User.id))
    user = db.relationship(User)

    add_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def dict(self):
        rst = {}
        rst['id'] = self.id
        rst['webhook_id'] = self.webhook_id
        rst['user_id'] = self.user_id
        rst['user'] = {}
        if self.user:
            rst['user'] = self.user.dict()
        rst['add_time'] = self.add_time
        return rst
