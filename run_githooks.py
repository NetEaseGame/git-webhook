#coding=utf-8
'''
Created on 2015年12月25日
@contact: http://www.atool.org
'''


from app import app
import os
from app.dbs.sqlite_utils import sqlite_info
from app.dbs import githooks_dbs, githook_histories_dbs, consts_dbs
from app.others import hook_tasks

if __name__ == '__main__':
    if not os.path.exists(sqlite_info.get('DB', 'git_hook_config.db')):
        githooks_dbs.create_tables()
        githook_histories_dbs.create_tables()
        consts_dbs.create_tables()
    
    #开启线程处理hook事件
    hook_tasks.do_hook_task()
    
    app.run('0.0.0.0', 10010, debug = True,  threaded = True)

