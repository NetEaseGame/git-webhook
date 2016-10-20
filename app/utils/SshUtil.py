# -*- coding: utf-8 -*-
'''
Created on 2016-8-2

@author: hustcc
'''
import paramiko
import StringIO
from app.utils import StringUtil
import re


def ssh_log_success(log, fail_regex='.*(fail|error|0)$'):
    matchObj = re.match(fail_regex, log, re.M | re.I | re.S)
    if matchObj:
        return False
    return True


# ssh to exec cmd
def do_ssh_cmd(ip, port, accout, pkey, shell, push_data='', timeout=300):
    try:
        port = int(port)
    except:
        port = 22
    
    pkey = pkey.strip() + '\n'  # 注意最后有一个换行
    
    pkey_file = StringIO.StringIO(pkey)
    private_key = paramiko.RSAKey.from_private_key(pkey_file)
    
    s = paramiko.SSHClient()
    
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    s.connect(ip, port, accout, pkey=private_key)
    
    cmd = cmd + (" '%s'" % push_data)
    stdin, stdout, stderr = s.exec_command(cmd, timeout=timeout)
    
    out = stdout.read()
    err = stderr.read()
    
    log = out or err  # log
    success = StringUtil.is_empty(err)  # 是否成功失败

    s.close()
    pkey_file.close()
    
    if success:
        success = ssh_log_success(log)
    
    return success, log
