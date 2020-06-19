from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound

from exchange.config import settings
from exchange.dal.pagination import MyPagination
from exchange.data_base import create_session
from exchange.exceptions import PaginationError, UsersDALException
from exchange.messages import Message
from exchange.models import Currency, Operation, User, UserCurrency
from exchange.operation_type import OperationType
from exchange.serialization import AbstractSerialize, serialize
from sqlalchemy.orm import Query, Session


def check_user_existence_and_get_if_exists(user_id: int, session: Session) -> User:
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UsersDALException('User does not exists')
    return user


def check_course_changes(
        last_change_time: datetime, last_time_when_course_was_known: datetime
) -> None:
    if last_time_when_course_was_known < last_change_time:
        raise UsersDALException('currency price was change, check new price')
    if last_time_when_course_was_known > datetime.now():
        raise UsersDALException('too early time')


class Strategy(ABC):
    @abstractmethod
    def invoke(
            self,
            currency: Currency,
            amount: Decimal,
            user: User,
            user_currency: UserCurrency,
    ) -> UserCurrency:
        pass


class OperationStrategy:
    def __init__(self) -> None:
        self._strategy: Optional[Strategy] = None

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def invoke(
            self,
            currency: Currency,
            amount: Decimal,
            user: User,
            user_currency: UserCurrency,
    ) -> UserCurrency:
        if self._strategy is None:
            raise TypeError()
        return self._strategy.invoke(currency, amount, user, user_currency)


class Sell(Strategy):
    def invoke(
            self,
            currency: Currency,
            amount: Decimal,
            user: User,
            user_currency: UserCurrency,
    ) -> UserCurrency:
        if user_currency is None:
            raise UsersDALException('You don`t have this currency at all')
        if user_currency.amount < amount:
            raise UsersDALException(
                f'You have {user_currency.amount} but want to sell {amount}'
            )
        user_currency.amount -= amount
        user.money += currency.selling_price * amount
        return user_currency


class Buy(Strategy):
    def invoke(
            self,
            currency: Currency,
            amount: Decimal,
            user: User,
            user_currency: UserCurrency,
    ) -> UserCurrency:
        money_change = currency.purchasing_price * amount
        if user.money < money_change:
            raise UsersDALException('You dont have money to make operation')
        user.money -= money_change
        if user_currency is None:
            user_currency = UserCurrency(
                user_id=user.id, currency_id=currency.id, amount=amount
            )
        else:
            user_currency.amount += amount
        return user_currency


class UsersDAL:
    @staticmethod
    def add_user(login: str) -> AbstractSerialize:
        with create_session() as session:
            if session.query(User).filter(User.login == login).first() is None:
                u = User(login=login, money=settings.start_money)
                session.add(u)
                session.flush()
                return serialize(u)
            raise UsersDALException(Message.USER_ALREADY_CREATED.value)

    @staticmethod
    def make_operation_with_currency(
            user_id: int,
            currency_id: int,
            operation: OperationType,
            amount: Decimal,
            time: datetime,
    ) -> AbstractSerialize:
        with create_session() as session:
            currency: Currency = session.query(Currency).filter(
                Currency.id == currency_id
            ).first()
            if currency is None:
                raise UsersDALException('currency does not exist')
            user = check_user_existence_and_get_if_exists(user_id, session)
            check_course_changes(currency.modified_at, time)
            user_currency: UserCurrency = session.query(UserCurrency).filter(
                UserCurrency.user_id == user_id, UserCurrency.currency_id == currency_id
            ).first()
            if amount <= 0:
                raise UsersDALException('Invalid amount')
            os = OperationStrategy()
            if operation == OperationType.BUY:
                os.set_strategy(Buy())
            else:
                os.set_strategy(Sell())
            user_currency = os.invoke(currency, amount, user, user_currency)
            session.add(user_currency)
            session.flush()
            copy = deepcopy(user_currency)
            if user_currency.amount == 0:
                session.delete(user_currency)
            operation = Operation(
                user_id=user_id,
                currency_id=currency_id,
                operation_type=operation,
                amount=amount,
                time=datetime.now(),
            )
            session.add(operation)
        return serialize(copy)

    @staticmethod
    def get_user_currencies(user_id: int) -> List[AbstractSerialize]:
        res: List[AbstractSerialize] = []
        with create_session() as session:
            check_user_existence_and_get_if_exists(user_id, session)
            user_currencies = (
                session.query(UserCurrency)
                    .filter(UserCurrency.user_id == user_id)
                    .all()
            )
            for user_currency in user_currencies:
                res.append(serialize(user_currency))
        return res

    @staticmethod
    def get_user_operations_history(
            user_id: int,
            operation_type: Optional[OperationType] = None,
            size: Optional[int] = None,
            page: Optional[int] = None,
    ) -> List[AbstractSerialize]:
        with create_session() as session:
            check_user_existence_and_get_if_exists(user_id, session)
            operations_query: Query = session.query(Operation).filter(
                Operation.user_id == user_id
            )
            if operation_type is not None:
                operations = operations_query.filter(
                    Operation.operation_type == operation_type
                ).all()
            else:
                operations = operations_query.all()
            if operations is None:
                raise UsersDALException('Cannot find operations with this parameters')
            if size is None and page is not None or size is not None and page is None:
                raise PaginationError('size or page not stated')
            if size is not None and page is not None:
                operations = MyPagination.get_pagination(operations, page, size)
            res = []
            for operation in operations:
                res.append(serialize(operation))
        return res

    @staticmethod
    def get_user_by_name(user_name: str) -> AbstractSerialize:
        with create_session() as session:
            try:
                user = session.query(User).filter(User.login == user_name).one()
                return serialize(user)
            except NoResultFound:
                raise UsersDALException()

    @staticmethod
    def get_user_by_id(user_id: int) -> AbstractSerialize:
        with create_session() as session:
            user = check_user_existence_and_get_if_exists(user_id, session)
            return serialize(user)
