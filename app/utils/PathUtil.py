#coding=utf-8
'''
Created on 2015年2月5日

@author: hustcc
'''
import os
import sys

def upload_dir():
    return _cur_file_dir() + '/app/static/upload/'

def log_dir():
    return _cur_file_dir() + '/log/'

def default_tmp_dir():
    return _cur_file_dir() + '/app/static/tmp/'

def _cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
    
if __name__ == '__main__':
    print _cur_file_dir()
