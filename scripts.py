# -*- coding: utf-8 -*-
'''
Created on 2016年6月15日

@author: hustcc
'''
import sys
from app import SQLAlchemyDB as db


def do_nothing():
    return 'nothing done.'


def rebuild_db():
    db.create_all()


def build_db():
    # database init
    db.drop_all()
    db.create_all()
    return 'build database success.'


# 定义一些操作
operator = {
    'build_db': build_db,
    'rebuild_db': rebuild_db,
}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('argv length is not equal 2.')
    else:
        print(operator.get(sys.argv[1], do_nothing)())
