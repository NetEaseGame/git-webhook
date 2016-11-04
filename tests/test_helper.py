# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from six import text_type
from schema import And, Use
from flask import Flask, jsonify
from app.utils import param
from . import load_data


def mock_get_data():
    return {
        'name': 'guyskk',
        'age': '21'
    }

schema = {
    'name': text_type,
    'age': And(Use(int), lambda x: 18 <= x <= 99)
}
expect = [123, 'guyskk', 21]


@param(schema, get_data=mock_get_data)
def index(user_id, name, age):
    return [user_id, name, age]


def test_basic():
    app = Flask(__name__)
    with app.test_request_context('/'):
        assert index(123) == expect
        assert index(user_id=123) == expect


def test_with_flask():
    app = Flask(__name__)

    @app.route('/user/<int:user_id>', methods=['POST'])
    @param(schema)
    def user(user_id, name, age):
        return jsonify(data=[user_id, name, age])

    with app.test_client() as c:
        resp = c.post('/user/123', data={'name': 'guyskk', 'age': 21})
        assert resp.status_code == 200
        assert load_data(resp) == expect

    with app.test_client() as c:
        resp = c.post('/user/123', data={'age': 21})
        assert resp.status_code == 400
        print(resp.data)

    with app.test_client() as c:
        resp = c.post('/user/123', data={'name': 'guyskk', 'age': 17})
        assert resp.status_code == 400
        print(resp.data)
