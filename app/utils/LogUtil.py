#coding=utf-8
'''
Created on 2015年8月24日

@author: hustcc
'''
from app.utils import PathUtil, DateUtil

def append_log(log_file, data):
    '''
    append data to file pathing with filePath
    '''
    if data:
        file_handler = open(PathUtil.log_dir() + log_file, 'a')
        file_handler.write(data + '\n')
        file_handler.close()
        
    return True

#记录非法用户的日志，一般这些用户都是尝试模拟请求的方式往数据库写入信息
def log_invalid(request, ext_text):
    log = '%s - - [%s] %s %s %s' % (request.remote_addr, DateUtil.now_datetime(), request.method, request.path, ext_text)
    append_log('record_invaild_log.log', log)