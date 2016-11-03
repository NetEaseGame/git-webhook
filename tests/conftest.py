# -*- coding: utf-8 -*-
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


@pytest.fixture
def user(sql):
    return create_user(sql)
