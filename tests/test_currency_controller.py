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
