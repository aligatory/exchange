import json
from http import HTTPStatus
from typing import Any

from flask import request
from flask_restplus import Namespace, Resource, fields, marshal

from .root_controller import error_fields

users_api: Namespace = Namespace('users', description='Users related operations')
user_fields = users_api.model('User', {'login': fields.String, 'money': fields.Float})
currency_fields = users_api.model(
    'Currencies',
    {'name': fields.String, 'operation': fields.String, 'amount': fields.Float},
)
operation_fields = users_api.model(
    'Operation',
    {
        'operation_type': fields.String,
        'currency': fields.String,
        'amount': fields.Float,
    },
)

currencies_operation_fields = users_api.model(
    'Currencies operation',
    {
        'currency_id': fields.Integer,
        'operation_type': fields.String,
        'amount': fields.Float,
        'time': fields.DateTime,
    },
)


@users_api.route('/')
@users_api.param('login', 'User login', required=True)
@users_api.response(HTTPStatus.OK, model=user_fields, description='Usser created')
@users_api.response(HTTPStatus.BAD_REQUEST, model=error_fields, description='Error')
class Users(Resource):
    def post(self) -> Any:
        # ошибка падает, если такой пользователь уже есть в системе
        # if a:
        #     return marshal({'login': '123', 'money': 123}, user_fields)
        return marshal({'message': 'error'}, error_fields)


@users_api.route('/<user_id>/currencies/')
@users_api.param('user_id', 'User id')
class UserCurrencies(Resource):
    @users_api.response(HTTPStatus.BAD_REQUEST, description='error', model=error_fields)
    @users_api.marshal_list_with(currency_fields, code=HTTPStatus.OK)
    def get(self, user_id: str) -> Any:
        # ошибка падает при невереном пользователе
        pass

    # @users_api.param('currency_id', description='Currency id')
    # @users_api.param('operation', description='Type of operation')
    # @users_api.param('amount', description='Amount')
    # @users_api.param('time', description='The time when the course was known')
    @users_api.response(
        HTTPStatus.CREATED, description='Operation done', model=currency_fields
    )
    @users_api.response(HTTPStatus.BAD_REQUEST, description='Error', model=error_fields)
    @users_api.expect(currencies_operation_fields)
    def post(self, user_id: str) -> Any:
        # a = request.json
        # ошибка будет при неправильном id пользоватлей или валюты,
        # при неправильном времени(больше текущего),
        # при ошибке при покупке, продаже(-баланс), при изменении курса
        pass


@users_api.route('/<user_id>/operations/')
@users_api.param('user_id', 'User id')
@users_api.param('operation_type', 'History by type of operation')
@users_api.param('size', 'Pagination page size')
@users_api.param('page', 'Pagination page')
class UserOperations(Resource):
    @users_api.marshal_list_with(operation_fields, code=HTTPStatus.OK)
    @users_api.response(HTTPStatus.BAD_REQUEST, 'Error', model=error_fields)
    def get(self, user_id: str) -> Any:
        # ошибка, если пользователь указан неверно, неправильно заданы параметры пагинации,
        # operation_type is invalid
        pass
