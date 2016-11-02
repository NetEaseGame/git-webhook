# -*- coding: utf-8 -*-
import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as c:
        yield c


def test_app(client):
    assert client.get("/").status_code == 200
