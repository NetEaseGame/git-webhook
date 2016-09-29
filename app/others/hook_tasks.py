#coding=utf-8
'''
Created on 2015年6月16日
all tasks
@author: hustcc
'''
from app.wraps.async_task_wrap import async_task
import os
import Queue
from app.dbs import githook_histories_dbs
from app.utils import HookDataParse, OtherUtil
from time import sleep

#github 上触发web hook的队列
web_hook_tasks = Queue.Queue(maxsize = 0)


def do_task(hook_info, data):
    '''
    ps：执行github pull，拉取代码，执行相应的shell重启服务
    need：校验hook_info和data的数据是否匹配
    '''
    cmd = hook_info.get('hook_sh', '')
    md5 = hook_info.get('md5', '')
    if cmd:
        if HookDataParse.get_repo_name(data) == hook_info.get('repo_name', ''):
            os.system(cmd)
            #shell output is in TODO list.
            githook_histories_dbs.add_history(md5, 'web hook success.', 'shell output is in TODO list.', HookDataParse.get_push_name(data), HookDataParse.get_push_email(data), '1', OtherUtil.object_2_dict(data))
        else:
            githook_histories_dbs.add_history(md5, 'hook repo_name is not match.', '', HookDataParse.get_push_name(data), HookDataParse.get_push_email(data), '0', OtherUtil.object_2_dict(data))
    else:
        githook_histories_dbs.add_history(md5, 'hook cmd is empty.', '', HookDataParse.get_push_name(data), HookDataParse.get_push_email(data), '0', OtherUtil.object_2_dict(data))
        
@async_task
def do_hook_task():
    global web_hook_tasks
    while True:
        hook_task = web_hook_tasks.get()
        hook_info = hook_task.get('hook_info', None)
        data = hook_task.get('data', None)
        if hook_task and hook_info and data:
            do_task(hook_info, data)
