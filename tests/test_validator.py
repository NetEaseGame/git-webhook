# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pytest
from schema import Use
from flask import Flask
from app.utils.validator import Validator
from app.utils.ResponseUtil import standard_response
from . import success, load_data

v = Validator()


@v.register('even')
def even():
    return Use(int, lambda value: value % 2)


SCHEMA = {
    'name': v.str(),
    'age': v.int(min=18, max=99),
    'sex': v.enum('男', '女'),
    'number': v.even(),
    v.optional('email'): v.email()
}
EXPECT = {
    'user_id': 123,
    'name': 'kk',
    'age': 21,
    'sex': '男',
    'number': 2,
    'email': 'validator@gmail.com'
}
DATA = {
    'name': 'kk',
    'age': '21',
    'sex': '男',
    'number': 2,
    'email': 'validator@gmail.com'
}
JSONDATA = json.dumps(DATA)

app = Flask(__name__)


@app.route('/<int:user_id>', methods=['GET', 'POST'])
@v.param(SCHEMA)
def index(**kwargs):
    return standard_response(1, kwargs)


@pytest.fixture
def client():
    with app.test_client() as c:
        yield c


# def load_data(resp):
#     if resp.status_code != 200:
#         print(resp.data)
#     assert resp.status_code == 200
#     return json.loads(resp.data)


def test_form_ok(client):
    resp = client.post('/123', data=DATA)
    assert load_data(resp) == EXPECT


def test_json_ok(client):
    headers = {'Content-Type': 'application/json'}
    resp = client.post('/123', data=JSONDATA, headers=headers)
    assert load_data(resp) == EXPECT


def test_args_ok(client):
    resp = client.get('/123', query_string=DATA)
    assert load_data(resp) == EXPECT


def test_optional(client):
    data = DATA.copy()
    data.pop('email')
    resp = client.post('/123', data=data)
    expect = EXPECT.copy()
    expect['email'] = None
    load_data(resp) == expect


def test_required(client):
    data = DATA.copy()
    data.pop('name')
    resp = client.post('/123', data=data)
    assert not success(resp)


def test_error(client):
    data = DATA.copy()
    data['age'] = '17'
    resp = client.post('/123', data=data)
    assert not success(resp)
