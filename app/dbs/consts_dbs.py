#coding=utf-8
'''
Created on 2015年11月24日

@author: hustcc
'''
from app.dbs.sqlite_utils import SqliteHandler
from app.utils import StringUtil, DateUtil


def get_password():
    '''
    info: 获取数据库中所有的redis信息
    '''
    sql = "select * from consts where key = 'password';"
    params = ()
    return SqliteHandler().exec_select_one(sql, params)


def insert_or_update_password(new_pwd):
    new_pwd = StringUtil.md5(new_pwd)
    add_time = DateUtil.now_datetime()
    
    password = get_password()
    if password:
        sql = "update consts set `value` = ?, add_time = ? where `key` = 'password';"
        params = (new_pwd, add_time)
        return SqliteHandler().exec_update(sql, params)
    else:
        sql = "insert into consts (`key`, `value`, add_time) values ('password', ?, ?)"
        params = (new_pwd, add_time)
        return SqliteHandler().exec_insert(sql, params)


def create_tables():
    '''
    info:创建表结构，第一次初始化的时候使用
    '''
    sql = ("create table consts("
           "key varchar, "
           "value varchar, "
           "add_time varchar)")
    SqliteHandler().exec_sql(sql, ())
    
if __name__ == '__main__':
    create_tables()