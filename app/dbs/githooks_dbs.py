#coding=utf-8
'''
Created on 2015年11月24日

@author: hustcc
'''
from app.dbs.sqlite_utils import SqliteHandler
from app.utils import StringUtil, DateUtil


def get_all_githooks():
    '''
    info: 获取数据库中所有的redis信息
    '''
    sql = "select * from git_hooks order by add_time desc;"
    params = ()
    return SqliteHandler().exec_select(sql, params)


def get_githook_by_md5(md5):
    sql = "select * from git_hooks where md5 = ?"
    params = (md5, )
    return SqliteHandler().exec_select_one(sql, params)


def get_githook_by_name(repo_name):
    sql = "select * from git_hooks where repo_name = ?"
    params = (repo_name, )
    return SqliteHandler().exec_select_one(sql, params)

def add_githook(repo_name, hook_sh):
    '''
    info: 添加一个redis信息到数据库
    '''
    add_time = DateUtil.now_datetime()
    md5 = StringUtil.md5(repo_name)
    r = get_githook_by_md5(md5)
    if r:
        #存在，update
        sql = "update git_hooks set repo_name = ?, hook_sh = ?, add_time = ? where md5 = ?"
        params = (repo_name, hook_sh, add_time, md5)
        return SqliteHandler().exec_update(sql, params)
    else:
        sql = "insert into git_hooks (repo_name, hook_sh, add_time, md5) values (?, ?, ?, ?)"
        params = (repo_name, hook_sh, add_time, md5)
        return SqliteHandler().exec_insert(sql, params)
    

def delete_hook(md5):
    '''
    info: delete hook information from db
    '''
    sql = "delete from git_hooks where md5 = ?"
    params = (md5, )
    return SqliteHandler().exec_update(sql, params)

def create_tables():
    '''
    info:创建表结构，第一次初始化的时候使用
    '''
    sql = ("create table git_hooks("
           "repo_name varchar, "
           "hook_sh varchar, "
           "add_time varchar, "
           "md5 varchar)")
    SqliteHandler().exec_sql(sql, ())
    
if __name__ == '__main__':
    create_tables()