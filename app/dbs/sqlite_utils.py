#coding=utf-8
'''
Created on 2015年10月27日
数据库操作类
@author: hustcc
'''
import sqlite3

sqlite_info = {
    'DB': 'git_hook_config.db',
}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqliteHandler():
    #对象属性
    #连接
    conn = None
    #数据游标
    cursor = None
    
    #构造函数
    def __init__(self, db = sqlite_info['DB']):
        self.db = db
        self.__connect()
    
    def __connect(self):
        try:
            self.conn = sqlite3.connect(self.db)
            self.conn.row_factory = dict_factory
            self.cursor = self.conn.cursor()
        except Exception, e:
            print e
    
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
    
    def exec_select(self, sql, params = ()):
        '''
        ps：执行查询类型的sql语句
        '''
        try:
            self.cursor.execute(sql, params)
            result_set = self.cursor.fetchall()
            return result_set
        except Exception, e:
            print e
            return False
        
    def exec_select_one(self, sql, params = ()):
        '''
        ps：执行查询类型的sql语句
        '''
        try:
            self.cursor.execute(sql, params)
            result_set = self.cursor.fetchone()
            return result_set
        except Exception, e:
            print e
            return False
    
    def exec_insert(self, sql, params = ()):
        '''
        ps:执行插入类sql语句
        '''
        try:
            # 执行sql语句
            self.cursor.execute(sql, params)
            # 提交到数据库执行
            insert_id = self.cursor.lastrowid
            self.conn.commit()
            return insert_id
        except Exception as e:
            print e
            self.conn.rollback()
            return False
    
    def exec_insert_many(self, sql, datas):
        try:
            # 执行sql语句
            self.cursor.executemany(sql, datas)
            # 提交到数据库执行
            row_count = self.cursor.rowcount
            self.conn.commit()
            return row_count
        except Exception, e:
            print e
            self.conn.rollback()
            return False
    
    def exec_update(self, sql, params = ()):
        '''
        ps:执行更新类sql语句
        '''
        try:
            # 执行sql语句
            self.cursor.execute(sql, params)
            row_count = self.cursor.rowcount
            # 提交到数据库执行
            self.conn.commit()
            if row_count == False:
                row_count = True
            return row_count
        except Exception, e:
            print e
            self.conn.rollback()
            return False
    
    def exec_sql(self, sql, params = ()):
        try:
            # 执行sql语句
            self.cursor.execute(sql, params)
            # 提交到数据库执行
            self.conn.commit()
            return True
        except Exception, e:
            print e
            self.conn.rollback()
            return False