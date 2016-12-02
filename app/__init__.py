# -*- coding: utf-8 -*-
'''
Created on 2015年6月16日

@author: hustcc
'''
import os
from flask import Flask
from flask_github import GitHub
from flask_sqlalchemy import SQLAlchemy
from celery import Celery, platforms
from app.utils.validator import Validator
from flask_socketio import SocketIO


# 版本号
__version__ = '0.0.6'


# flask
app = Flask(__name__)
app.config.from_object('app.config_default')

# 加载默认 home 目录配置 git_webhook_config.py
config_file = os.path.join(os.path.expanduser('~'),
                           '.git-webhook/git_webhook_config.py')
if 'GIT_WEBHOOK_CONFIG' in os.environ:
    app.config.from_envvar('GIT_WEBHOOK_CONFIG')
elif os.path.exists(config_file):
    app.config.from_pyfile(config_file)
else:
    # 最后从代码目录加载配置
    try:
        # 兼容老的写法
        app.config.from_object('app.config')
    except:
        app.config.from_object('app.config_example')


socketio = SocketIO(app,
                    message_queue=app.config['SOCKET_MESSAGE_QUEUE'])

# validator
v = Validator()

# flask-sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SQLAlchemyDB = SQLAlchemy(app)


# celery
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


platforms.C_FORCE_ROOT = True
celeryInstance = make_celery(app)


# github login
github = GitHub(app)

from app.database import model  # noqa
from app import views  # noqa
