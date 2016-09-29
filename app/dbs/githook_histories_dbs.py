#coding=utf-8
'''
Created on 2015年12月30日

@author: hustcc
'''
from app.dbs.sqlite_utils import SqliteHandler
from app.utils import DateUtil


def add_history(md5, notice, output, push_name, push_email, success, data):
    add_time = DateUtil.now_datetime()
    sql = "insert into githook_histories (md5, notice, output, push_name, push_email, success, add_time, data) values (?, ?, ?, ?, ?, ?, ?, ?);"
    params = (md5, notice, output, push_name, push_email, success, add_time, data)
    return SqliteHandler().exec_insert(sql, params)


def get_repo_histories(md5):
    sql = "select rowid, md5, notice, output, push_name, push_email, success, add_time from githook_histories where md5 = ? order by add_time desc;"
    params = (md5, )
    return SqliteHandler().exec_select(sql, params)


def get_hook_data_by_rowid(rowid):
    sql = "select rowid, md5, push_name, push_email, success, add_time, data from githook_histories where rowid = ?;"
    params = (rowid, )
    return SqliteHandler().exec_select_one(sql, params)

def create_tables():
    '''
    info:创建表结构，第一次初始化的时候使用
    '''
    sql = ("create table githook_histories("
           "md5 varchar, " #外键
           "notice varchar, "
           "output varchar, "
           "push_name varchar, "
           "push_email varchar, "
           "success varchar, "
           "data varchar, "
           "add_time varchar)")
    
    SqliteHandler().exec_sql(sql, ())
    