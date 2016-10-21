#coding=utf-8
'''
Created on 2015年6月16日

@author: hustcc
'''
from flask import Flask
from app import config

# flask
app = Flask(__name__)
app.secret_key = 'your_session_key_git_webhook'

# flask sqlachemt
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SQLAlchemyDB = SQLAlchemy(app)
from app.database import model


# celery
from celery import Celery, platforms
platforms.C_FORCE_ROOT = True
app.config['CELERY_BROKER_URL'] = config.CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = config.CELERY_RESULT_BACKEND
celeryInstance = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celeryInstance.conf.update(app.config)


# github login
from flask_github import GitHub
app.config['GITHUB_CLIENT_ID'] = config.GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = config.GITHUB_CLIENT_SECRET
github = GitHub(app)

# import views
from app import views
