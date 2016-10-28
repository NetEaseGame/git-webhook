# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.wraps.login_wrap import login_required
from app import app
from app.utils import ResponseUtil, RequestUtil, SshUtil
from app.database.model import Server


# get server list
@app.route('/api/server/list', methods=['GET'])
@login_required()
def api_server_list():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    
    servers = Server.query.filter_by(user_id=user_id, deleted=False).all()
    servers = [server.dict(with_pkey=True) for server in servers]
    
    return ResponseUtil.standard_response(1, servers)


# new server
@app.route('/api/server/new', methods=['POST'])
@login_required()
def api_server_new():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    
    ip = RequestUtil.get_parameter('ip', '')
    name = RequestUtil.get_parameter('name', ip)
    name = name and name or ip
    port = RequestUtil.get_parameter('port', 22)
    account = RequestUtil.get_parameter('account', '')
    pkey = RequestUtil.get_parameter('pkey', '')
    
    if not all((ip, name, port, account, pkey)):
        return ResponseUtil.standard_response(0, 'Form data can not be blank!')
    
    try:
        success, log = SshUtil.do_ssh_cmd(ip, port, account, pkey, 'ls -lh', timeout=5)
        if success:
            server_id = RequestUtil.get_parameter('id', '')
            if server_id:
                # update webhook
                # you can only update the webhook which you create.
                server = Server.query.filter_by(id=server_id, user_id=user_id).first()
                if not server:
                    return ResponseUtil.standard_response(0, 'Server is not exist!')
                server.ip = ip
                server.port = port
                server.account = account
                server.pkey = pkey
                server.name = name
            else:
                server = Server(ip=ip, port=port, account=account, pkey=pkey,
                                user_id=user_id, name=name)

            server.save()

            return ResponseUtil.standard_response(1, server.dict(with_pkey=True))
    except Exception, e:
        print e
    return ResponseUtil.standard_response(0, 'Server SSH connect error!')


@app.route('/api/server/delete', methods=['POST'])
@login_required()
def api_server_delete():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    server_id = RequestUtil.get_parameter('server_id', '')

    server = Server.query.filter_by(user_id=user_id, id=server_id).first()
    if not server:
        return ResponseUtil.standard_response(0, 'Permition deny!')

    server.deleted = True
    server.save()

    return ResponseUtil.standard_response(1, 'Success')
