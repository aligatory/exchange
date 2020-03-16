from copy import copy

from exchange.api.serialization import AbstractSerialize, Serializer, UserOutputFields
from exchange.data_base import create_session
from exchange.exceptions import UsersDALException
from exchange.messages import Message
from exchange.models import User


class UsersDAL:
    @staticmethod
    def add_user(login: str) -> AbstractSerialize:
        with create_session() as session:
            if session.query(User).filter(User.login == login).first() is None:
                u = User(login=login, money=1000)
                u_copy = copy(u)
                session.add(u)
            else:
                raise UsersDALException(Message.USER_ALREADY_CREATED.value)
        return Serializer.serialize(u_copy, UserOutputFields)
