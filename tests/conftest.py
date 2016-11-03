# -*- coding: utf-8 -*-
import mock
import pytest
from app import app as _app, SQLAlchemyDB
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
