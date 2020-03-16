import json
from http import HTTPStatus

from exchange.config import START_MONEY
from exchange.data_base import create_session
from exchange.models import User
from flask import Response
from flask.testing import FlaskClient


def test_add_user(client: FlaskClient):
    login = 'test'
    response: Response = client.post(
        '/users/', data=json.dumps(dict(login=login)), content_type='application/json'
    )
    assert response.status_code == HTTPStatus.CREATED
    with create_session() as session:
        res: User = session.query(User).filter(User.id == 1).first()
        assert res.money == START_MONEY
        assert res.login == login
