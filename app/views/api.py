# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app import app
from app.utils import RequestUtil, HookDataParse, JsonUtil
from app.tasks import tasks
from flask.globals import request
import json
from app.database.model import WebHook, History


@app.route('/api/git-webhook/<key>', methods=['POST', 'GET'])
def api_for_webhook(key):
    '''git hook data
    '''
#     try:
    data = RequestUtil.get_parameter('hook', None)
    if data is None:
        data = request.data

#     for test
#     data = WebhookData.github
#     data = WebhookData.gitlab
#     data = WebhookData.gitosc
    try:
        data = json.loads(data)
        webhook = WebHook.query.filter_by(key=key).first()
        if webhook:
            repo = webhook.repo
            branch = webhook.branch

            # then repo and branch is match the config. then do the shell
            if (HookDataParse.get_repo_name(data) == repo and
                    HookDataParse.get_repo_branch(data) == branch):
                # start to process, add history into database
                # waiting to done
                history = History(webhook_id=webhook.id,
                                  data=JsonUtil.object_2_json(data))
                history.updateStatus('1')
                # status is waiting
                webhook.updateStatus('1')
                # do the async task
                tasks.do_webhook_shell.delay(webhook.id, history.id, data)
                return "Work put into Queue."

            return "Not match the Repo and Branch."
        else:
            return "The webhook is not exist."
    except Exception as e:
        return "Request is not valid Git webhook: " + str(e)
