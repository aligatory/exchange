from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm as so

engine = sa.create_engine()
Session = sessionmaker(bind=engine)
Base: Any = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, unique=True)
    money = sa.Column(sa.DECIMAL)
    user_currency = so.relationship('user_currency', backref='user')
    operation = so.relationship('operation',backref='user')


class UserCurrency(Base):
    __tablename__ = 'user_currency'
    id = sa.Column(sa.Integer, primary_key=True)
    # user = so.relationship(User, back_populates='user_currency', uselist=True)
    currency = so.relationship('currency', backref='user_currency')
    amount = sa.Column(sa.DECIMAL)


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    purchase_price = sa.Column(sa.DECIMAL)
    selling_price = sa.Column(sa.DECIMAL)
    last_change_time = sa.Column(sa.DateTime)
    # user_currency = so.relationship(UserCurrency, back_populates='currency', uselist=False)

class Operation(Base):
    __tablename__ = 'operation'
    id = sa.Column(sa.Integer, primary_key=True)
    # user = so.relationship(User,back)
