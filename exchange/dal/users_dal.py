from dataclasses import dataclass
from decimal import Decimal

from exchange.data_base import create_session
from exchange.exceptions import UsersDALException
from exchange.messages import Message
from exchange.models import User


@dataclass
class UserToReturn:
    login: str
    money: Decimal


class UsersDAL:
    @staticmethod
    def add_user(login: str) -> UserToReturn:
        with create_session() as session:
            if session.query(User).filter(User.login == login).first() is None:
                u = User(login=login, money=1000)
                session.add(u)
                return UserToReturn(u.login, Decimal(u.money))
            else:
                raise UsersDALException(Message.USER_ALREADY_CREATED.value)
