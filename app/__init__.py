# -*- coding: utf-8 -*-
'''
Created on 2015年6月16日

@author: hustcc
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# flask
app = Flask(__name__)
app.config.from_object('app.config_default')

# 加载配置
if 'GIT_WEBHOOK_CONFIG' in os.environ:
    app.config.from_envvar('GIT_WEBHOOK_CONFIG')
else:
    app.config.from_object('app.config')

# flask-sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
SQLAlchemyDB = SQLAlchemy(app)
from app.database import model

# celery
from celery import Celery, platforms
platforms.C_FORCE_ROOT = True
celeryInstance = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celeryInstance.conf.update(app.config)

# github login
from flask_github import GitHub
github = GitHub(app)

# import views
from app import views
