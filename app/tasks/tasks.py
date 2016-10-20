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
def do_webhook_shell(webhook, push_data):
    ip = webhook.get('server', {}).get('ip', '')
    port = webhook.get('server', {}).get('port', '22')
    account = webhook.get('server', {}).get('account', '')
    pkey = webhook.get('server', {}).get('pkey', '')
    
    shell = webhook.get('shell', '')
    
    repo = webhook.get('repo', '')
    branch = webhook.get('branch', '')
    
    # start to process, add history into database
    history = History(status='1', webhook_id=webhook.get('id', 0), data=push_data)
    history.save()
    
    webhookObj = WebHook.query.get(webhook.get('id', 0))
    webhookObj.status = '1'
    webhookObj.save()
    
    # then repo and branch is match the config. then do the shell
    if HookDataParse.get_repo_name(push_data) == repo and \
        HookDataParse.get_repo_branch(push_data) == branch:
        try:
            success, log = SshUtil.do_ssh_cmd(ip, port, accout, pkey, shell, JsonUtil.object_2_json(push_data))
            history.status = '2'
            webhookObj.status = '2'
            if success:
                history.status = '3'
                webhookObj.status = '3'
        except:
            success, log = False, 'Server SSH error'
            history.status = '4'
            webhookObj.status = '4'
        
        history.push_user = '%s <%s>' % (HookDataParse.get_push_name(data), HookDataParse.get_push_email(data))
        history.shell_log = log
        history.save()
        webhookObj.save()
    else:
        history.shell_log = 'Repo name and branch can not match with the webhook config.'
