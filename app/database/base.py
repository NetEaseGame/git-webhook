# -*- coding: utf-8 -*-
'''
Created on 2016年10月2日

@author: CXM
'''
from app import SQLAlchemyDB as db


# 一些公共的方法，仅仅适合单独操作，对于事务操作，还是需要手工写db.session代码
class BaseMethod(object):
    __table_args__ = {'mysql_engine':'MyISAM', 'mysql_charset':'utf8'}
    # insert and update
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()
