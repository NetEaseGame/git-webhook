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

# 版本号
__version__ = '0.0.1'

# flask
app = Flask(__name__)
app.config.from_object('app.config_default')

# 加载配置
if 'GIT_WEBHOOK_CONFIG' in os.environ:
    app.config.from_envvar('GIT_WEBHOOK_CONFIG')
else:
    app.config.from_object('app.config')

# validator
v = Validator()

# flask-sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
SQLAlchemyDB = SQLAlchemy(app)

# celery
platforms.C_FORCE_ROOT = True
celeryInstance = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celeryInstance.conf.update(app.config)

# github login
github = GitHub(app)

from app.database import model  # noqa
from app import views  # noqa
