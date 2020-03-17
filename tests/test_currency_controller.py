import json
from http import HTTPStatus

from flask import Response
from flask.testing import FlaskClient


def test_add_currency(client: FlaskClient):
    name: str = 'bitcoin'
    purchasing_price: int = 228
    selling_price: int = 2
<<<<<<< HEAD
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
=======
    response: Response = client.post('/currencies/', data=json.dumps(
        dict(name=name, purchasing_price=purchasing_price, selling_price=selling_price)))
>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
    assert response.status_code == HTTPStatus.CREATED
    j = response.json
    assert j['id'] == 1
    assert j['name'] == name
