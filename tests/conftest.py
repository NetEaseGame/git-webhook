# -*- coding: utf-8 -*-
import mock
import pytest
from app import app as _app, SQLAlchemyDB
from app.database import model
from app.utils import RequestUtil
import app.utils.SshUtil as ssh
from .import success, load_data

# =====================================
# base fixtures
# =====================================


@pytest.fixture
def app():
    SQLAlchemyDB.create_all()
    yield _app
    SQLAlchemyDB.session.close()
    SQLAlchemyDB.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture
def sql(app):
    return SQLAlchemyDB.session


@pytest.fixture
def tester(app, sql):
    """模拟已登录用户"""
    with app.test_client() as c:
        user = create_user(sql)
        mock_func = mock.MagicMock(return_value=user.dict())
        with mock.patch.object(RequestUtil, 'get_login_user', new=mock_func):
            yield c


def create_user(sql):
    user_id = 'tester'
    user = model.User(
        id=user_id,
        name=user_id,
        location='',
        avatar=''
    )
    sql.add(user)
    sql.commit()
    return user

# =====================================
# server fixtures
# =====================================
SERVER_DATA = {
    'ip': '127.0.0.1',
    'name': 'dev',
    'port': '22',
    'account': 'root',
    'pkey': 'asdfghjkl',
}


def mock_do_ssh_cmd(*args, **kwargs):
    return True, "OK"


@pytest.fixture
def create_server(tester):
    def func(**kwargs):
        data = SERVER_DATA.copy()
        data.update(kwargs)
        with mock.patch.object(ssh, 'do_ssh_cmd', new=mock_do_ssh_cmd):
            resp = tester.post('/api/server/new', data=data)
            assert success(resp)
        return load_data(resp)
    return func

# =====================================
# webhook fixtures
# =====================================
WEBHOOK_DATA = {
    'repo': 'test_repo',
    'branch': 'master',
    'shell': 'echo hello',
}


@pytest.fixture
def create_webhook(tester):
    def func(**kwargs):
        data = WEBHOOK_DATA.copy()
        data.update(kwargs)
        resp = tester.post('/api/webhook/new', data=data)
        assert success(resp)
        return load_data(resp)
    return func
