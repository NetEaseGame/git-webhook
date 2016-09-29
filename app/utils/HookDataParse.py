#coding=utf-8
'''
Created on 2015年12月30日

@author: hustcc
'''

#仓库名称
def get_repo_name(hook_data):
    return hook_data.get('repository', {}).get('name', '') or hook_data.get('push_data', {}).get('repository', {}).get('name', '')

#push人的名字
def get_push_name(hook_data):
    uid = hook_data.get('pusher', {}).get('name', None) #github的data格式
    if uid:
        return uid
    uid = hook_data.get('user_name', None) #gitlib 格式
    if uid:
        return uid

    uid = hook_data.get('push_data', {}).get('user', {}).get('name', None) #gitosc的data格式
    if uid:
        return uid
    return ''

def get_push_email(hook_data):
    uid = hook_data.get('pusher', {}).get('email', None) #github的data格式
    if uid:
        return uid
    uid = hook_data.get('user_email', None) #gitlib 格式
    if uid:
        return uid
    
    uid = hook_data.get('push_data', {}).get('user', {}).get('email', None) #gitosc的data格式
    if uid:
        return uid
    return ''