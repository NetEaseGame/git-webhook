# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.wraps.login_wrap import login_required
from app import app, v
from app.utils import ResponseUtil, RequestUtil, AuthUtil
from app.database.model import Collaborator, User


# get server list
@app.route('/api/collaborator/list', methods=['GET'])
@login_required()
@v.param({'webhook_id': v.int()})
def api_collaborator_list(webhook_id):
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')

    if not AuthUtil.has_readonly_auth(user_id, webhook_id):
        return ResponseUtil.standard_response(0, 'Permition deny!')

    collaborators = Collaborator.query.filter_by(webhook_id=webhook_id).all()
    collaborators = [collaborator.dict() for collaborator in collaborators]

    return ResponseUtil.standard_response(1, collaborators)


# new server
@app.route('/api/collaborator/new', methods=['POST'])
@login_required()
@v.param({'webhook_id': v.int(), 'user_id': v.str()})
def api_collaborator_new(webhook_id, user_id):
    # login user
    login_user_id = RequestUtil.get_login_user().get('id', '')

    if not AuthUtil.has_admin_auth(login_user_id, webhook_id):
        return ResponseUtil.standard_response(0, 'Permition deny!')

    collaborator = Collaborator.query.filter_by(webhook_id=webhook_id,
                                                user_id=user_id).first()

    # not exist
    if collaborator:
        return ResponseUtil.standard_response(0, 'Collaborator exist!')

    # 开始添加
    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id, name=user_id)
        user.save()
    collaborator = Collaborator(webhook_id=webhook_id, user=user)

    collaborator.save()

    return ResponseUtil.standard_response(1, collaborator.dict())


@app.route('/api/collaborator/delete', methods=['POST'])
@login_required()
@v.param({'collaborator_id': v.int()})
def api_collaborator_delete(collaborator_id):
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')

    collaborator = Collaborator.query.get(collaborator_id)
    if not collaborator:
        return ResponseUtil.standard_response(0, 'Permition deny!')

    webhook_id = collaborator.webhook_id

    if not AuthUtil.has_admin_auth(user_id, webhook_id):
        return ResponseUtil.standard_response(0, 'Permition deny!')

    collaborator.delete()

    return ResponseUtil.standard_response(1, 'Success')
