# -*- coding: utf-8 -*-
'''
Created on 2015-6-16

@author: hustcc
'''

import hashlib
import binascii
import uuid


def is_empty(s):
    '''string is empty ?'''
    if s is None or s == '':
        return True
    return False


def is_true(s):
    '''string is true'''
    if s is True:
        return True
    if s == 'true':
        return True
    return False


def md5_salt(s, salt="webhook"):
    '''
    md5 + 盐：即便两个用户使用了同一个密码，由于系统为它们生成的salt值不同，他们的散列值也是不同的。
    '''
    if s:
        return md5(s + salt)
    else:
        return ''


def md5(s):
    '''
    md5
    '''
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def crc32_hash(v):
    """
    Generates the crc32 hash of the v.
    @return: str, the str value for the crc32 of the v (crc32b)
    """
    return '%x' % (binascii.crc32(v) & 0xffffffff)  # 取crc32的八位数据 %x返回16进制


def md5_token(salt=None):
    s = str(uuid.uuid1())
    if salt:
        return md5_salt(s, salt)
    return md5(s)


# 获取一个新的token，保证完全唯一
def crc32_token():
    return crc32_hash(str(uuid.uuid1()).encode('utf-8'))
