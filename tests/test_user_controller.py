import json
from datetime import datetime
from http import HTTPStatus
from time import sleep

import pytest
from exchange.config import settings
from exchange.data_base import create_session
from exchange.models import User
from flask import Response
from flask.testing import FlaskClient


def test_add_user(client: FlaskClient, user_login):
    response: Response = client.post(
        '/users/',
        data=json.dumps(dict(login=user_login)),
        content_type='application/json',
    )
    assert response.status_code == HTTPStatus.CREATED
    with create_session() as session:
        res: User = session.query(User).filter(User.id == 1).first()
        assert res.money == settings.start_money
        assert res.login == user_login


@pytest.mark.usefixtures('_add_user')
def test_get_user(client: FlaskClient, user_login):
    response: Response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json['login'] == user_login


@pytest.mark.usefixtures('_add_user', '_add_currency')
def test_buy_currency(client: FlaskClient):
    sleep(1)
    response: Response = client.post(
        '/users/1/currencies/',
        data=json.dumps(
            dict(
                currency_id=1,
                operation='BUY',
                amount='1',
                time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            )
        ),
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json['amount'] == '1.00000'


@pytest.fixture()
def _buy_currency(client):
    sleep(1)
    client.post(
        '/users/1/currencies/',
        data=json.dumps(
            dict(
                currency_id=1,
                operation='BUY',
                amount='1',
                time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            )
        ),
    )


@pytest.mark.usefixtures('_add_user', '_add_currency', '_buy_currency')
def test_get_user_operations(client: FlaskClient):
    response: Response = client.get('/users/1/operations/')
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert len(response_json) == 1
    assert response_json[0]['amount'] == '1.00000'
    assert response_json[0]['operation_type'] == 'BUY'


@pytest.mark.usefixtures('_add_user', '_add_currency', '_buy_currency')
def test_get_user_currencies(client: FlaskClient):
    response: Response = client.get('/users/1/currencies/')
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert len(response_json) == 1
    assert response_json[0]['currency_id'] == 1
    assert response_json[0]['amount'] == '1.00000'
