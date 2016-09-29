#coding=utf-8
'''
Created on 2015年6月16日

@author: hustcc
'''
from app import app
import flask
from app.utils import RequestUtil, OtherUtil, HookDataParse
from flask.globals import request
from app.dbs import githooks_dbs, githook_histories_dbs, consts_dbs
import sys
from app.others import hook_tasks
import json
from app.wraps.has_set_pwd_wrap import has_set_pwd
from app.wraps.trace_wrap import log_traceback

reload(sys)
sys.setdefaultencoding('utf-8') 


@app.route('/', methods=['GET'])
@has_set_pwd
@log_traceback
def index_page():
    githooks = githooks_dbs.get_all_githooks()
    url_root = request.url_root
    return flask.render_template('index_page.html', githooks = githooks, url_root = url_root)


@app.route('/history/<md5>', methods=['GET'])
@has_set_pwd
@log_traceback
def history_page(md5):
    githook = githooks_dbs.get_githook_by_md5(md5)
    githook_histories = githook_histories_dbs.get_repo_histories(md5)
    if githook:
        return flask.render_template('history_page.html', githook = githook, githook_histories = githook_histories)
    return "repo hook is not exist."

@app.route('/data/<rowid>.html', methods=['GET'])
@has_set_pwd
@log_traceback
def pre_data_page(rowid):
    hook_data = githook_histories_dbs.get_hook_data_by_rowid(rowid)
    if hook_data:
        return flask.render_template('hook_data_page.html', hook_data = hook_data)
    return "repo hook history is not exist."

@app.route('/set_pwd', methods=['GET'])
def set_pwd():
    password = consts_dbs.get_password()
    if password:
        is_reset = True
    else:
        is_reset = False
    return flask.render_template('set_pwd.html', is_reset = is_reset, password = password)


@app.route('/api/set_pwd', methods=['GET', 'POST'])
def api_set_pwd():
    old_password = RequestUtil.get_parameter(request, 'old_password', '')
    new_password = RequestUtil.get_parameter(request, 'new_password', '')
    re_password = RequestUtil.get_parameter(request, 're_password', '')
    next_url = RequestUtil.get_parameter(request, 'next', request.url_root)
    rst = {}
    
    if new_password != re_password:
        rst = {'success': 0, 'data': 'two inputs are not match.'}
        return OtherUtil.object_2_dict(rst)
    
    password = consts_dbs.get_password()
    if password and old_password:
        #验证旧密码
        if OtherUtil.md5(old_password) != password.get('value', ''):
            rst = {'success': 0, 'data': 'old password is not match.'}
            return OtherUtil.object_2_dict(rst)
        #就密码正确，更新密码
        consts_dbs.insert_or_update_password(new_password)
    else:
        #没有设置过密码，则新建密码
        consts_dbs.insert_or_update_password(new_password)
    
    rst = {'success': 1, 'data': next_url}
    return OtherUtil.object_2_dict(rst)

@app.route('/api/del', methods=['GET', 'POST'])
def del_hook():
    hook_md5 = RequestUtil.get_parameter(request, 'md5', '')
    pwd = RequestUtil.get_parameter(request, 'password', '')
    password = consts_dbs.get_password()
    
    if OtherUtil.md5(pwd) == password.get('value', ''):
        rid = githooks_dbs.delete_hook(hook_md5)
        if rid:
            rst = {'success': 1, 'data': ''}
        else:
            rst = {'success': 0, 'data': 'del hook error'}
        return OtherUtil.object_2_dict(rst)
    else:
        return OtherUtil.object_2_dict({'success': 0, 'data': 'password not match.'})
    

@app.route('/api/add', methods=['GET', 'POST'])
def add_hook():
    repo_name = RequestUtil.get_parameter(request, 'repo_name', '')
    githook_sh = RequestUtil.get_parameter(request, 'githook_sh', '')
    pwd = RequestUtil.get_parameter(request, 'password', '')
    password = consts_dbs.get_password()
    
    if OtherUtil.md5(pwd) == password.get('value', ''):
        if not repo_name:
            return OtherUtil.object_2_dict({'success': 0, 'data': 'repo_name is empty.'})
        rid = githooks_dbs.add_githook(repo_name, githook_sh)
        if rid:
            rst = {'success': 1, 'data': ''}
        else:
            rst = {'success': 0, 'data': 'add / update hook error.'}
        return OtherUtil.object_2_dict(rst)
    else:
        return OtherUtil.object_2_dict({'success': 0, 'data': 'password not match.'})
    

@app.route('/api/hook/<md5>', methods=['POST'])
def for_hook(md5):
    '''
    git hook data
    '''
    try:
        data = RequestUtil.get_parameter(request, 'hook', None)
        if data == None:
            data = request.data

        data = json.loads(data)
        hook_info = githooks_dbs.get_githook_by_md5(md5)
        if hook_info:
            #add to task queue
            hook_task = {'hook_info': hook_info, 'data': data}
            hook_tasks.web_hook_tasks.put(hook_task)
            return "hook add to task success."
        else:
            githook_histories_dbs.add_history(md5, 'md5 is not valid.', '', HookDataParse.get_push_name(data), HookDataParse.get_push_email(data), '0', request.data)
            return "md5 is not valid."
    except Exception, e:
        print e
        return "not a valid git web hook request."

#定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return '404'

@app.errorhandler(502)
def server_502_error(error):
    return '502'

@app.route('/not_allow', methods=['GET'])
def deny(error):
    return 'You IP address is not in white list...'