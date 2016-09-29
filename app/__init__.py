#coding=utf-8
'''
Created on 2015年6月16日

@author: hustcc
'''
from flask import Flask

app = Flask(__name__)
app.secret_key = 'your_session_key_git_hooks'

from app.views import main_views