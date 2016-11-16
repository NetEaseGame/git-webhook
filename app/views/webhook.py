# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''

from app.wraps.login_wrap import login_required
from app import app
from app.utils import ResponseUtil, RequestUtil, StringUtil, JsonUtil, AuthUtil
from app.database.model import WebHook, Server, History, Collaborator
from app.tasks import tasks
from sqlalchemy.sql.expression import false


# get webhook list
@app.route('/api/webhook/list', methods=['GET'])
@login_required()
def api_webhook_list():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')

    # create webhooks
    created_webhooks = WebHook.query.filter_by(user_id=user_id,
                                               deleted=False).all()

    # collaborator webhooks
    collaborated_webhooks = \
        WebHook.query.join(Collaborator,
                           Collaborator.webhook_id == WebHook.id) \
                     .filter(Collaborator.user_id == user_id) \
                     .filter(WebHook.deleted == false()).all()

    webhooks = created_webhooks + collaborated_webhooks
    # to dict
    webhooks = {'id%s' % webhook.id: webhook for webhook in webhooks}
    # value
    webhooks = webhooks.values()
    # sort
    sorted(webhooks, key=lambda webhook: webhook.id)
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
        return ResponseUtil.standard_response(0, 'Permission deny!')

    repo = RequestUtil.get_parameter('repo', '')
    branch = RequestUtil.get_parameter('branch', '')
    shell = RequestUtil.get_parameter('shell', '')

    if not all((repo, branch, shell, server_id)):
        return ResponseUtil.standard_response(0, 'Form data can not be blank!')

    webhook_id = RequestUtil.get_parameter('id', '')
    if webhook_id:
        webhook = AuthUtil.has_admin_auth(user_id, webhook_id)
        if not webhook:
            return ResponseUtil \
                .standard_response(0, 'WebHook not exist or Permission deny!')
        webhook.repo = repo
        webhook.branch = branch
        webhook.shell = shell
        webhook.server_id = server_id
    else:
        # new webhook
        webhook = WebHook(
            repo=repo,
            branch=branch,
            shell=shell,
            server_id=server_id,
            user_id=user_id,
            key=StringUtil.md5_token()
        )

    webhook.save()

    return ResponseUtil.standard_response(1, webhook.dict(with_key=True))


@app.route('/api/webhook/delete', methods=['POST'])
@login_required()
def api_webhook_delete():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    webhook_id = RequestUtil.get_parameter('webhook_id', '')

    # 验证创建者权限
    webhook = AuthUtil.has_admin_auth(user_id, webhook_id)
    if not webhook:
        return ResponseUtil.standard_response(0, 'Permission deny!')

    webhook.deleted = True
    webhook.save()

    return ResponseUtil.standard_response(1, 'Success')


@app.route('/api/webhook/retry', methods=['POST'])
@login_required()
def api_webhook_retry():
    # login user
    user_id = RequestUtil.get_login_user().get('id', '')
    webhook_id = RequestUtil.get_parameter('webhook_id', '')

    data = {
        'src': 'Manually executed'
    }
    webhook = WebHook.query.get(webhook_id)
    if not webhook:
        return ResponseUtil.standard_response(0, 'WebHooknot exist!')

    if not AuthUtil.has_readonly_auth(user_id, webhook_id):
        return ResponseUtil.standard_response(0, 'Permission deny!')

#     if webhook.status not in ['3', '4', '5']:
#         return ResponseUtil.standard_response(0, 'Webhook is Executing!')

    history = History(webhook_id=webhook.id,
                      data=JsonUtil.object_2_json(data))
    history.updateStatus('1')
    # status is waiting
    webhook.updateStatus('1')
    # do the async task
    tasks.do_webhook_shell.delay(webhook.id, history.id, data, user_id=user_id)

    return ResponseUtil.standard_response(1, webhook.dict())
