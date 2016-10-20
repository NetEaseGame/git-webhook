# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.wraps.login_wrap import login_required
from app import app
from app.utils import ResponseUtil, RequestUtil
from app.database.model import Server

# get server list
@app.route('/api/server/list', methods=['GET'])
@login_required()
def api_server_list():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    
    servers = Server.query.filter(user_id=user_id).all()
    servers = [server.dict() for server in servers]
    
    return ResponseUtil.standard_response(1, servers)


# new server
@app.route('/api/server/new', methods=['POST'])
@login_required()
def api_server_new():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    
    ip = RequestUtil.get_parameter('ip', '')
    name = RequestUtil.get_parameter('name', ip)
    port = RequestUtil.get_parameter('port', 22)
    account = RequestUtil.get_parameter('account', '')
    shell = RequestUtil.get_parameter('shell', '')
    pkey = RequestUtil.get_parameter('pkey', '')
    
    if not all((ip, name, port, account, shell, pkey)):
        return ResponseUtil.standard_response(0, 'Form data can not be blank!')
    
    server = Server(ip=ip, port=port, shell=shell, account=account, pkey=pkey, 
                      user_id=user_id, name=name)
    
    server.save()
    
    return ResponseUtil.standard_response(1, webhook.dict())


@app.route('/api/server/delete', methods=['POST'])
@login_required()
def api_server_delete():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    server_id = RequestUtil.get_parameter('server_id', '')
    
    server = Server.query.filter(user_id=user_id, id=server_id)
    if not server:
        return ResponseUtil.standard_response(0, 'Permition deny!')
    
    server.delete()
    
    return ResponseUtil.standard_response(1, 'Success')
