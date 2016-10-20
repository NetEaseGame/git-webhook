#coding=utf-8
'''
Created on 2015年12月30日

@author: hustcc
'''

# repo name
def get_repo_name(hook_data):
    return hook_data.get('repository', {}).get('name', '') or hook_data.get('push_data', {}).get('repository', {}).get('name', '')


# repo branch
def get_repo_branch(hook_data):
    branch = hook_data.get('ref', '') # github, gitlib
    if branch:
        return branch[branch.rfind("/"):]
    return hook_data.get('push_data', {}).get('ref', '') # gitosc


# push user name
def get_push_name(hook_data):
    uid = hook_data.get('pusher', {}).get('name', None) # github的data格式
    if uid:
        return uid
    uid = hook_data.get('user_name', None) # gitlib 格式
    if uid:
        return uid

    uid = hook_data.get('push_data', {}).get('user', {}).get('name', None) # gitosc的data格式
    if uid:
        return uid
    return ''

# push user email
def get_push_email(hook_data):
    uid = hook_data.get('pusher', {}).get('email', None) # github的data格式
    if uid:
        return uid
    uid = hook_data.get('user_email', None) # gitlib 格式
    if uid:
        return uid
    
    uid = hook_data.get('push_data', {}).get('user', {}).get('email', None) # gitosc的data格式
    if uid:
        return uid
    return ''