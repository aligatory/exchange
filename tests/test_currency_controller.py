import json
from http import HTTPStatus
from typing import NamedTuple

import pytest
from flask import Response
from flask.testing import FlaskClient


def test_add_currency(client: FlaskClient):
    name: str = 'bitcoin'
    purchasing_price: str = '228'
    selling_price: str = '2'
    response: Response = client.post(
        '/currencies/',
        data=json.dumps(
            dict(
                name=name,
                purchasing_price=purchasing_price,
                selling_price=selling_price,
            )
        ),
    )
    assert response.status_code == HTTPStatus.CREATED
    j = response.json
    assert j['id'] == 1
    assert j['name'] == name


class CurrencyParams(NamedTuple):
    name: str
    purchasing_price: str
    selling_price: str


@pytest.fixture()
def currency_params():
    return CurrencyParams('1', '2.28', '2.82')


@pytest.fixture()
def _add_currency(client, currency_params):
    client.post(
        '/currencies/',
        data=json.dumps(
            dict(
                name=currency_params.name,
                purchasing_price=currency_params.purchasing_price,
                selling_price=currency_params.selling_price,
            )
        ),
    )


@pytest.mark.usefixtures('_add_currency')
def test_get_currency_by_id(client: FlaskClient, currency_params):
    response: Response = client.get('/currencies/1/')
    assert response.status_code == HTTPStatus.OK
    j = json.loads(response.data)
    assert j['name'] == currency_params.name
    assert j['purchasing_price'] == '2.28000'
    assert j['selling_price'] == '2.82000'


@pytest.mark.usefixtures('_add_currency')
def test_get_currency_history(client: FlaskClient, currency_params):
    response: Response = client.get('/currencies/1/history/')
    assert response.status_code == HTTPStatus.OK
    assert response.json[0]['selling_price'] == '2.82000'
    assert response.json[0]['purchasing_price'] == '2.28000'


def test_get_currency_history_with_invalid_path_param(client: FlaskClient):
    response: Response = client.get('/currencies/a/history/')
    assert response.status_code == HTTPStatus.BAD_REQUEST
