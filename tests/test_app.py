# -*- coding: utf-8 -*-
import mock
import pytest
from flask import redirect, session
from app import app as _app, github, SQLAlchemyDB
from app.database import model
from app.utils import RequestUtil


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
def user(sql):
    return create_user()


def test_app(client):
    assert client.get("/").status_code == 200


def test_login(client):
    def mock_post(*args, **kwargs):
        response = mock.Mock()
        response.content = b'access_token=mocktoken&token_type=bearer'
        return response

    def mock_get_user(*args, **kwargs):
        return {'login': 'mock_userid'}

    @mock.patch.object(github, 'get', new=mock_get_user)
    @mock.patch.object(github.session, 'post', new=mock_post)
    def mock_authorize(*args, **kwargs):
        client.get('/github/callback?code=mockcode')
        return redirect('/')

    @mock.patch.object(github, 'authorize', new=mock_authorize)
    def test():
        client.get('/login')
        assert session['oauth_token'] == 'mocktoken'

    test()


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
    RequestUtil.login_user(user.dict())
    return user
