# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app import celeryInstance
from app.database.model import History, WebHook
from app.utils import SshUtil, JsonUtil, HookDataParse


# webhook / data all is JSON dict.
@celeryInstance.task
def do_webhook_shell(webhook_id, histroy_id, data):
    webhook = WebHook.query.get(webhook_id)
    history = History.query.get(histroy_id)
    # server information
    ip = webhook.server.ip
    port = webhook.server.port
    account = webhook.server.account
    pkey = webhook.server.pkey
    
    # do what
    shell = webhook.shell
    
    # start to process, add history into database
    status = '2'
    history.updateStatus(status)
    webhook.updateStatus(status)
    try:
        success, log = SshUtil.do_ssh_cmd(ip, port, account, pkey, shell, JsonUtil.object_2_json(data))
        status = '3' # error
        if success:
            status = '4' # success
    except Exception, e:
        success, log = False, 'Server SSH error: ' + str(e)
        status = '5' # except

    history.status = status
    history.push_user = '%s <%s>' % (HookDataParse.get_push_name(data), HookDataParse.get_push_email(data))
    history.shell_log = log
    history.save()
    
    webhook.updateStatus(status)
