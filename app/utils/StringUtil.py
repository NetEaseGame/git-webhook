#coding=utf-8
'''
Created on 2015年6月16日

@author: hustcc
'''
import hashlib

def is_empty(s):
    if s == None or s == '':
        return True
    return False


def md5(s):
    if not s:
        s = ''
    m = hashlib.md5()   
    m.update(s)   
    return m.hexdigest() 