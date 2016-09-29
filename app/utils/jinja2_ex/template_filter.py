#coding=utf-8
'''
Created on 2015年5月6日

@author: hustcc
'''
from app import app

@app.context_processor
def ext_jinja2_processor():
    '''
    ps:扩展jinja2的内置方法
    '''
    def str_sub(s, start, end, suffix = None):
        '''
        str_sub；字符串截断
        '''
        if suffix:
            return s[start:end] + suffix
        return s[start:end]
    
    def str_len(s):
        '''
        str_len：字符串长度
        '''
        return len(s)
    
    def to_str(i):
        '''
        to_str：将数字转字符串，一些比较的时候会使用到
        '''
        return str(i)
    
    def to_round(f, d = 3):
        '''
        to_round：浮点数小数位数
        '''
        return round(f, d)
    
    return dict(str_sub = str_sub, str_len = str_len, to_str = to_str, to_round = to_round)
