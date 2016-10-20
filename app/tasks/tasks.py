# -*- coding: utf-8 -*-
'''
Created on 2016-10-20

@author: hustcc
'''
from app.database.model import History
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
    
    # then repo and branch is match the config. then do the shell
    if HookDataParse.get_repo_name(push_data) == repo and \
        HookDataParse.get_repo_branch(push_data) == branch:
        success, log = SshUtil.do_ssh_cmd(ip, port, accout, pkey, shell, JsonUtil.object_2_json(push_data))
        
        history.status = '2'
        if success:
            history.status = '3'
        
        history.push_user = '%s <%s>' % (HookDataParse.get_push_name(data), HookDataParse.get_push_email(data))
        history.shell_log = log
        history.save()
    else:
        history.shell_log = 'Repo name and branch can not match with the webhook config.'
