# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''

from app.wraps.login_wrap import login_required
from app import app
from app.utils import ResponseUtil, RequestUtil, StringUtil
from app.database.model import WebHook, Server

# get webhook list
@app.route('/api/webhook/list', methods=['GET'])
@login_required()
def api_webhook_list():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    
    webhooks = WebHook.query.filter_by(user_id=user_id).all()
    webhooks = [webhook.dict(True) for webhook in webhooks]
    
    return ResponseUtil.standard_response(1, webhooks)


# new webhook
@app.route('/api/webhook/new', methods=['POST'])
@login_required()
def api_webhook_new():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    server_id = RequestUtil.get_parameter('server_id', '')
    # server must be added by yourself
    if not Server.query.filter_by(id=server_id, user_id=user_id).first():
        return ResponseUtil.standard_response(0, 'Permition deny!')
    
    repo = RequestUtil.get_parameter('repo', '')
    branch = RequestUtil.get_parameter('branch', '')
    shell = RequestUtil.get_parameter('shell', '')
    
    if not all((repo, branch, shell, server_id)):
        return ResponseUtil.standard_response(0, 'Form data can not be blank!')
    
    webhook = WebHook(repo=repo, branch=branch, shell=shell, server_id=server_id, 
                      user_id=user_id, key=StringUtil.md5_token())
    
    webhook.save()
    
    return ResponseUtil.standard_response(1, webhook.dict())


@app.route('/api/webhook/delete', methods=['POST'])
@login_required()
def api_webhook_delete():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    webhook_id = RequestUtil.get_parameter('webhook_id', '')
    
    webhook = WebHook.query.filter_by(user_id=user_id, id=webhook_id).first()
    if not webhook:
        return ResponseUtil.standard_response(0, 'Permition deny!')
    
    webhook.delete()
    
    return ResponseUtil.standard_response(1, 'Success')
