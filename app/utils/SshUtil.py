# -*- coding: utf-8 -*-
'''
Created on 2016-8-2

@author: hustcc
'''
import paramiko
import StringIO


def is_log_success(log):
    for x in ['fatal', 'fail', 'error']:
        if log.startswith(x) or log.endswith(x):
            return False
    return True


# ssh to exec cmd
def do_ssh_cmd(ip, port, account, pkey, shell, push_data='', timeout=300):
    try:
        port = int(port)
    except:
        port = 22

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 首先以 ssh 密钥方式登陆
        pkey_file = StringIO.StringIO(pkey.strip() + '\n')  # 注意最后有一个换行
        private_key = paramiko.RSAKey.from_private_key(pkey_file)
        s.connect(ip, port, account, pkey=private_key, timeout=5)
        pkey_file.close()
    except:
        # 如果出现异常，则使用 用户密码登陆的方式
        s.connect(ip, port, account, password=pkey, timeout=5)

#     if push_data:
#     shell = shell + (" '%s'" % push_data)
    shell = shell.split('\n')
    shell = [sh for sh in shell if sh.strip()]
    shell = ' && '.join(shell)

    stdin, stdout, stderr = s.exec_command(shell, timeout=timeout)

    log = stdout.read()
    err = stderr.read()

    success = True
    if not log and err:
        success = False
        log = err

    s.close()

    if success:
        success = is_log_success(log)

    return success, log
