# -*- coding: utf-8 -*-
import json
import pytest
from app.database import model
from . import WEBHOOKDATA, success, load_data


def test_server_new(tester, create_server):
    resp = tester.post('/api/server/new', data={})
    assert not success(resp)
    server = create_server()
    assert server['ip'] == '127.0.0.1'


def test_server_delete(tester, create_server, sql):
    server = create_server()
    resp = tester.post('/api/server/delete', data={'server_id': server['id']})
    assert success(resp)
    text = 'select count(*) from server where !deleted'
    assert sql.execute(text).scalar() == 0


def test_server_list(tester, create_server):
    create_server()
    create_server()
    resp = tester.get('/api/server/list')
    assert success(resp)
    assert len(load_data(resp)) == 2


def test_webhoot_new(tester, create_server, create_webhook):
    server = create_server()
    webhook = create_webhook(server_id=server['id'])
    assert webhook['branch'] == 'master'
    webhook = create_webhook(server_id=server['id'],
                             webhook_id=webhook['id'], branch='dev')
    assert webhook['branch'] == 'dev'


def test_webhoot_delete(tester, create_server, create_webhook, sql):
    server = create_server()
    webhook = create_webhook(server_id=server['id'])
    data = {'webhook_id': webhook['id']}
    resp = tester.post('/api/webhook/delete', data=data)
    assert success(resp)
    text = 'select count(*) from web_hook where !deleted'
    assert sql.execute(text).scalar() == 0


def test_webhook_list(tester, create_server, create_webhook):
    server = create_server()
    create_webhook(server_id=server['id'])
    create_webhook(server_id=server['id'])
    resp = tester.get('/api/webhook/list')
    assert success(resp)
    assert len(load_data(resp)) == 2


def test_history(tester, create_server, create_webhook, sql):
    server = create_server()
    webhook = create_webhook(server_id=server['id'])

    query_string = {'webhook_id': webhook['id']}
    resp = tester.get('/api/history/list', query_string=query_string)
    assert len(load_data(resp)['histories']) == 0

    history = model.History(
        status='1',
        webhook_id=webhook['id'],
        data='null'
    )
    sql.add(history)
    sql.commit()

    resp = tester.get('/api/history/list', query_string=query_string)
    assert len(load_data(resp)['histories']) == 1


@pytest.mark.parametrize("name,data", WEBHOOKDATA.items())
def test_git_webhook(tester, create_server, create_webhook, name, data):
    server = create_server()
    webhook = create_webhook(server_id=server['id'])
    url = '/api/git-webhook/{}'.format(webhook['key'])
    resp = tester.post(url, data=json.dumps(data))
    assert b'Work put into Queue' in resp.data
