from decimal import Decimal
from typing import Any, Optional

import sqlalchemy as sa
from exchange.data_base import Base
from exchange.operation_type import OperationType
from sqlalchemy import CheckConstraint, Integer, TypeDecorator
from sqlalchemy import orm as so


class SqliteDecimal(TypeDecorator):
    def process_literal_param(self, value: Any, dialect: Any) -> None:
        raise NotImplementedError()

    @property
    def python_type(self) -> None:
        raise NotImplementedError()

    # This TypeDecorator use Sqlalchemy Integer as impl. It converts Decimals
    # from Python to Integers which is later stored in Sqlite database.
    impl = Integer

    def __init__(self, scale: int) -> None:
        # It takes a 'scale' parameter, which specifies the number of digits
        # to the right of the decimal point of the number in the column.
        TypeDecorator.__init__(self)
        self.scale = scale
        self.multiplier_int = 10 ** self.scale

    def process_bind_param(
        self, value: Optional[Decimal], dialect: Any
    ) -> Optional[int]:
        # e.g. value = Column(SqliteDecimal(2)) means a value such as
        # Decimal('12.34') will be converted to 1234 in Sqlite
        if value is not None:
            return int(value * self.multiplier_int)
        return value

    def process_result_value(
        self, value: Optional[int], dialect: Any
    ) -> Optional[Decimal]:
        # e.g. Integer 1234 in Sqlite will be converted to Decimal('12.34'),
        # when query takes place.
        if value is not None:
            return Decimal(value) / self.multiplier_int
        return value


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, unique=True)
    money = sa.Column(SqliteDecimal(10), CheckConstraint('money>=0'))
    user_currencies = so.relationship(
        'UserCurrency', back_populates='user', uselist=False
    )
    operation = so.relationship('Operation', back_populates='user', uselist=False)


class UserCurrency(Base):
    __tablename__ = 'user_currency'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False, index=True)
    currency_id = sa.Column(
        sa.Integer, sa.ForeignKey('currency.id'), nullable=False, index=True
    )
    amount = sa.Column(SqliteDecimal(10), CheckConstraint('amount>=0'))

    user = so.relationship(User, back_populates='user_currencies', uselist=False)
    currency = so.relationship('Currency', back_populates=__tablename__, uselist=False)


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    purchasing_price = sa.Column(
        SqliteDecimal(10), CheckConstraint('purchasing_price >0')
    )
    selling_price = sa.Column(SqliteDecimal(10), CheckConstraint('selling_price >0'))
    modified_at = sa.Column(sa.DateTime)

    user_currency = so.relationship(
        UserCurrency, back_populates=__tablename__, uselist=False
    )
    operation = so.relationship(
        'Operation', back_populates=__tablename__, uselist=False
    )


class Operation(Base):
    __tablename__ = 'operation'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False, index=True)
    currency_id = sa.Column(
        sa.Integer, sa.ForeignKey('currency.id'), nullable=False, index=True
    )
    operation_type = sa.Column(sa.Enum(OperationType))
    amount = sa.Column(SqliteDecimal(10), CheckConstraint('amount>=0'))
    time = sa.Column(sa.DateTime)

    user = so.relationship(User, back_populates=__tablename__, uselist=True)
    currency = so.relationship(Currency, back_populates=__tablename__, uselist=True)
