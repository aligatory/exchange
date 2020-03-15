from typing import Any

import sqlalchemy as sa
from exchange.data_base import Database
from exchange.operation_type import OperationType
from sqlalchemy import CheckConstraint
from sqlalchemy import orm as so

Base: Any = Database.base


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, unique=True)
    money = sa.Column(sa.DECIMAL, CheckConstraint('money>=0'))
    user_currencies = so.relationship(
        'UserCurrency', back_populates='user', uselist=False
    )
    operation = so.relationship('Operation', back_populates='user', uselist=False)


class UserCurrency(Base):
    __tablename__ = 'user_currency'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False, index=True)
    user = so.relationship(User, back_populates='user_currencies', uselist=False)
    currency_id = sa.Column(
        sa.Integer, sa.ForeignKey('currency.id'), nullable=False, index=True
    )
    currency = so.relationship('Currency', back_populates=__tablename__, uselist=False)
    amount = sa.Column(sa.DECIMAL, CheckConstraint('amount>=0'))


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    purchasing_price = sa.Column(sa.DECIMAL, CheckConstraint('purchasing_price >=0'))
    selling_price = sa.Column(sa.DECIMAL, CheckConstraint('selling_price >=0'))
    last_change_time = sa.Column(sa.DateTime)
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
    user = so.relationship(User, back_populates=__tablename__, uselist=True)
    currency_id = sa.Column(
        sa.Integer, sa.ForeignKey('currency.id'), nullable=False, index=True
    )
    currency = so.relationship(Currency, back_populates=__tablename__, uselist=True)
    operation_type = sa.Column(sa.Enum(OperationType))
    amount = sa.Column(sa.DECIMAL, CheckConstraint('amount>=0'))
