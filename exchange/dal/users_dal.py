from copy import deepcopy
from decimal import Decimal

from exchange.api.serialization import AbstractSerialize, Serializer, UserOutputFields
from exchange.data_base import create_session
from exchange.exceptions import UsersDALException
from exchange.messages import Message
from exchange.models import User
from exchange.config import START_MONEY
from exchange.operation_type import OperationType


class UsersDAL:
    @staticmethod
    def add_user(login: str) -> AbstractSerialize:
        with create_session() as session:
            if session.query(User).filter(User.login == login).first() is None:
                u = User(login=login, money=START_MONEY)
                session.add(u)
                session.flush()
                u_copy = deepcopy(u)
            else:
                raise UsersDALException(Message.USER_ALREADY_CREATED.value)
        return Serializer.serialize(u_copy, UserOutputFields)

    @staticmethod
    def make_operation_with_currency(user_id: int, currency_id: int, operation: OperationType,
                                     amount: Decimal) -> AbstractSerialize:
        pass
