# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.wraps.login_wrap import login_required
from app import app, v
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
@v.param({
    'ip': v.ipv4(),
    'port': v.int(min=0),
    'account': v.str(),
    'pkey': v.str(),
    v.optional('name'): v.str(),
    v.optional('id'): v.str()
})
def api_server_new(ip, port, account, pkey, name=None, id=None):
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    server_id = id
    name = name if name else ip

    try:
        success, log = SshUtil.do_ssh_cmd(
            ip, port, account, pkey, 'ls -lh', timeout=5)
        if success:
            if server_id:
                # update webhook
                # you can only update the webhook which you create.
                server = Server.query.filter_by(
                    id=server_id, user_id=user_id).first()
                if not server:
                    return ResponseUtil.standard_response(
                        0, 'Server is not exist!')
                server.ip = ip
                server.port = port
                server.account = account
                server.pkey = pkey
                server.name = name
            else:
                server = Server(ip=ip, port=port, account=account, pkey=pkey,
                                user_id=user_id, name=name)

            server.save()

            return ResponseUtil.standard_response(
                1, server.dict(with_pkey=True))
    except Exception as e:
        print(e)
    return ResponseUtil.standard_response(0, 'Server SSH connect error!')


@app.route('/api/server/delete', methods=['POST'])
@login_required()
@v.param({'server_id': v.int()})
def api_server_delete(server_id):
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    server = Server.query.filter_by(user_id=user_id, id=server_id).first()
    if not server:
        return ResponseUtil.standard_response(0, 'Permition deny!')

    server.deleted = True
    server.save()

    return ResponseUtil.standard_response(1, 'Success')
