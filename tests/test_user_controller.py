from flask.testing import FlaskClient


def test_add_user(client: FlaskClient):
    client.post()
