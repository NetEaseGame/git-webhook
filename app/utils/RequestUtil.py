#coding=utf-8
'''
Created on 2015年8月21日

@author: hustcc
'''

#获得参数，post或者get
def get_parameter(request, key, default = None):
    '''
    info:获得请求参数，包括get和post，其他类型的访问不管
    '''
    #post参数
    if request.method == 'POST':
        param = request.form.get(key, default)
    #get
    elif request.method == 'GET':
        param = request.args.get(key, default)
    else:
        return default
    
    return param

#用户IP
def get_request_ip(request):
    return request.remote_addr

#获得用户访问方式
def get_request_method(request):
    return request.method

def get_request_ua(request):
    return request.headers.get('User-Agent', '')

def get_request_accept_lang(request):
    request.environ.get('HTTP_ACCEPT_LANGUAGE', '')
