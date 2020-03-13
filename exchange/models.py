from typing import Any

import sqlalchemy as sa
from mypy_extensions import KwArg
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import orm as so
from sqlalchemy.util.compat import contextmanager

from exchange.operation_type import OperationType

import pathlib

Base: Any = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, unique=True)
    money = sa.Column(sa.DECIMAL)
    user_currencies = so.relationship('UserCurrency', back_populates=__tablename__, uselist=False)
    operation = so.relationship('Operation', back_populates=__tablename__, uselist=False)


class UserCurrency(Base):
    __tablename__ = 'user_currency'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False, index=True)
    user = so.relationship(User, back_populates="user_currencies", uselist=False)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey("currency.id"), nullable=False, index=True)
    currency = so.relationship('Currency', back_populates=__tablename__, uselist=False)
    amount = sa.Column(sa.DECIMAL)


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    purchase_price = sa.Column(sa.DECIMAL)
    selling_price = sa.Column(sa.DECIMAL)
    last_change_time = sa.Column(sa.DateTime)
    user_currency = so.relationship(UserCurrency, back_populates=__tablename__, uselist=False)

    operation = so.relationship('Operation', back_populates=__tablename__, uselist=False)


class Operation(Base):
    __tablename__ = 'operation'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False, index=True)
    user = so.relationship(User, back_populates=__tablename__, uselist=True)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey('currency.id'), nullable=False, index=True)
    currency = so.relationship(Currency, back_populates=__tablename__, uselist=True)
    operation_type = sa.Column(sa.Enum(OperationType))
    amount = sa.Column(sa.DECIMAL)


cur_path = pathlib.Path("my.db").resolve()
engine = sa.create_engine("sqlite:////" + str(cur_path))
my_session = sessionmaker(bind=engine)


@contextmanager
def create_session(**kwargs: Any) -> Session:
    new_session = my_session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


Base.metadata.create_all(engine)
with create_session() as session:
    # u = User(login="evg")
    # session.add(u)
    a: UserCurrency = session.query(UserCurrency).filter(UserCurrency.user_id == 2).first()
    print(a.user)
    print()
    # c = Currency(name="crypt12333",purchase_price=1234,selling_price=12)
    # session.add(c)
    # a = UserCurrency(user_id=2, currency_id=2,amount=123)
    # session.add(a)
