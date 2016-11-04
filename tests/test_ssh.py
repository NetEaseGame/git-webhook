# -*- coding: utf-8 -*-
import mock
from StringIO import StringIO
from contextlib import contextmanager
from paramiko import SSHClient
import app.utils.SshUtil as ssh
from . import RSA_PRIVATE_KEY


@contextmanager
def patch_ssh(stdout='', stderr=''):
    def mock_exec_command(*args, **kwargs):
        stdin = StringIO()
        stdin.close()
        return stdin, StringIO(stdout), StringIO(stderr)
    with mock.patch.object(SSHClient, 'exec_command', new=mock_exec_command):
        with mock.patch.object(SSHClient, 'connect'):
            yield


def test_ssh():
    kwargs = dict(
        ip='127.0.0.1',
        port='22',
        account='root',
        pkey=RSA_PRIVATE_KEY,
        shell='echo hello\n echo hello'
    )
    with patch_ssh('', ''):
        success, log = ssh.do_ssh_cmd(**kwargs)
        assert success
    with patch_ssh('', 'message'):
        success, log = ssh.do_ssh_cmd(**kwargs)
        assert not success
        assert 'message' in log
    msg = ('fatal: Not a git repository '
           '(or any parent up to mount point /tmp)\n'
           'Stopping at filesystem boundary '
           '(GIT_DISCOVERY_ACROSS_FILESYSTEM not set).')
    with patch_ssh(msg, ''):
        success, log = ssh.do_ssh_cmd(**kwargs)
        assert not success
        assert msg in log
