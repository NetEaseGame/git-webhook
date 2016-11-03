# -*- coding: utf-8 -*-
import mock
import json
import app.utils.SshUtil as ssh


def mock_do_ssh_cmd(*args, **kwargs):
    return True, "OK"


def success(response):
    if response.status_code == 200:
        print(response.data)
        data = json.loads(response.data)
        return data['success']
    return False


def load_data(response):
    data = json.loads(response.data)
    return data['data']

SERVER_DATA = {
    'ip': '127.0.0.1',
    'name': 'dev',
    'port': '22',
    'account': 'root',
    'pkey': 'asdfghjkl',
}


def create_server(tester):
    with mock.patch.object(ssh, 'do_ssh_cmd', new=mock_do_ssh_cmd):
        resp = tester.post('/api/server/new', data=SERVER_DATA)
        assert success(resp)
    return load_data(resp)


def test_server_new(tester):
    resp = tester.post('/api/server/new', data=SERVER_DATA)
    assert not success(resp)
    server = create_server(tester)
    assert server['ip'] == '127.0.0.1'


def test_server_delete(tester, sql):
    server = create_server(tester)
    resp = tester.post('/api/server/delete', data={'server_id': server['id']})
    assert success(resp)
    # TODO 是否需要彻底删除，而不是标记为删除
    text = 'select count(*) from server where !deleted'
    assert sql.execute(text).scalar() == 0


def test_server_list(tester):
    create_server(tester)
    create_server(tester)
    resp = tester.get('/api/server/list')
    assert success(resp)
    assert len(load_data(resp)) == 2

WEBHOOK_DATA = {
    'repo': 'test_repo',
    'branch': 'master',
    'shell': 'echo hello',
}


def create_webhook(tester, **kwargs):
    data = WEBHOOK_DATA.copy()
    data.update(kwargs)
    resp = tester.post('/api/webhook/new', data=data)
    assert success(resp)
    return load_data(resp)


def test_webhoot_new(tester):
    server = create_server(tester)
    webhook = create_webhook(tester, server_id=server['id'])
    assert webhook['branch'] == 'master'
    webhook = create_webhook(tester, server_id=server['id'],
                             webhook_id=webhook['id'], branch='dev')
    assert webhook['branch'] == 'dev'


def test_webhoot_delete(tester, sql):
    server = create_server(tester)
    webhook = create_webhook(tester, server_id=server['id'])
    data = {'webhook_id': webhook['id']}
    resp = tester.post('/api/webhook/delete', data=data)
    assert success(resp)
    text = 'select count(*) from web_hook where !deleted'
    assert sql.execute(text).scalar() == 0


def test_webhook_list(tester):
    server = create_server(tester)
    create_webhook(tester, server_id=server['id'])
    create_webhook(tester, server_id=server['id'])
    resp = tester.get('/api/webhook/list')
    assert success(resp)
    assert len(load_data(resp)) == 2
