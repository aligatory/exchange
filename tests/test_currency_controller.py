import json
from http import HTTPStatus

from flask import Response
from flask.testing import FlaskClient


def test_add_currency(client: FlaskClient):
    name: str = 'bitcoin'
    purchasing_price: int = 228
    selling_price: int = 2
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


def test_get_currency_by_id(client: FlaskClient):
    name = '1'
    purchasing_price = 2.28
    selling_price = 2.82
    client.post(
        '/currencies/',
        data=json.dumps(
            dict(
                name=name,
                purchasing_price=purchasing_price,
                selling_price=selling_price,
            )
        ),
    )
    response: Response = client.get('/currencies/1/')
    assert response.status_code == HTTPStatus.OK
    j = json.loads(response.data)
    assert j['name'] == name
    assert j['purchasing_price'] == '2.28000'
    assert j['selling_price'] == '2.82000'
