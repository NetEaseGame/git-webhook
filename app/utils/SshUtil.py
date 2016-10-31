# -*- coding: utf-8 -*-
'''
Created on 2016-8-2

@author: hustcc
'''
import paramiko
import StringIO
from app.utils import StringUtil
import re


def ssh_log_success(log):
    if log.endswith('fail') or log.endswith('error'):
        return False
    return True


# ssh to exec cmd
def do_ssh_cmd(ip, port, account, pkey, shell, push_data='', timeout=300):
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
    
    s.connect(ip, port, account, pkey=private_key)
#     if push_data:
#     shell = shell + (" '%s'" % push_data)
    shell = shell.split('\n')
    shell = [sh for sh in shell if sh.strip()]
    shell = ' && '.join(shell)
    
    stdin, stdout, stderr = s.exec_command(shell, timeout=timeout)
    
    out = stdout.read()
    err = stderr.read()

    log = '%s%s' % (out, err)  # log
    success = True

    s.close()
    pkey_file.close()
    
    if success:
        success = ssh_log_success(log)
    
    return success, log


if __name__ == '__main__':
    log = '''Fetching origin
HEAD is now at ce22661 测试webhook
sending incremental file list
app/static/upload/
app/views/

sent 2816 bytes  received 47 bytes  5726.00 bytes/sec
total size is 13095640  speedup is 4574.10

Sync done!
aibq: stopped
aibq: started
ssh_exchange_identification: Connection closed by remote host
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
error: Could not fetch origin
2016/10/31 11:27:03.338397 [INFO] qbox.us/qrsync/v3/qrsync/qrsync.go:50: Syncing /home/wwwroot/aibq/app/static => aibq
2016/10/31 11:27:03.338797 [INFO] qbox.us/qrsync/v3/qrsync/qrsync.go:119: Processing /root/.qrsync/MzCuBkLNxLMr-by4yydKmN6_.dbfail'''
    print ssh_log_success(log)