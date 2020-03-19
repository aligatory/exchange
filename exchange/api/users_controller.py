import json
from http import HTTPStatus
from typing import Any, Dict

from exchange.api.custom_fields import String, Decimal, OperationType as OTField, Integer
from exchange.api.root_controller import error_fields
from exchange.api.validation import (
    get_dict_from_json,
    validate_request_json,
    validate_path_parameter,
    validate_request_params,
)
from exchange.dal.users_dal import UsersDAL
from exchange.exceptions import UsersDALException, ValidationException
from exchange.operation_type import OperationType
from flask import request


from flask_restplus import Namespace, Resource, fields, marshal

users_api: Namespace = Namespace('users', description='Users related operations')

user_input_fields = users_api.model('User', {'login': String(required=True)})

user_output_fields = users_api.inherit(
    'UserInput', user_input_fields, {'money': fields.Fixed}
)

currency_output_fields = users_api.model(
    'Currencies',
    {
        'id': fields.Integer,
        'name': fields.String,
        'operation': fields.String,
        'amount': fields.Fixed,
    },
)

currency_input_fields = users_api.model(
    'InputCurrencies',
    {
        'id': Integer(required=True),
        'operation': OTField(required=True),
        'amount': Decimal(required=True)
    })
operation_fields = users_api.model(
    'Operation',
    {
        'operation_type': fields.String,
        'currency': fields.String,
        'amount': fields.Fixed,
    },
)

currency_operation_fields = users_api.model(
    'Currencies operation',
    {
        'currency_id': fields.Integer,
        'operation_type': fields.String,
        'amount': fields.Fixed,
        'time': fields.DateTime,
    },
)


@users_api.route('/')
@users_api.expect(user_input_fields)
@users_api.response(
    HTTPStatus.CREATED, model=user_output_fields, description='User created'
)
@users_api.response(HTTPStatus.BAD_REQUEST, model=error_fields, description='Error')
class Users(Resource):
    def post(self) -> Any:
        try:
            validated_json = validate_request_json(request.data, user_input_fields)
            return (
                marshal(
                    UsersDAL.add_user(validated_json['login']), user_output_fields
                ),
                HTTPStatus.CREATED,
            )
        except (ValidationException, UsersDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST


@users_api.route('/<user_id>/currencies/')
@users_api.param('user_id', 'User id')
class UserCurrencies(Resource):
    @users_api.response(HTTPStatus.BAD_REQUEST, description='error', model=error_fields)
    @users_api.marshal_list_with(currency_output_fields, code=HTTPStatus.OK)
    def get(self, user_id: str) -> Any:
        # parser.add_argument('user_id', type=int, help='user id must be int')
        # user_id_in_int: int = parser.parse_args()['user_id']
        # ошибка падает при невереном пользователе
        pass

    # @users_api.param('currency_id', description='Currency id')
    # @users_api.param('operation', description='Type of operation')
    # @users_api.param('amount', description='Amount')
    # @users_api.param('time', description='The time when the course was known')
    @users_api.response(
        HTTPStatus.CREATED, description='Operation done', model=currency_output_fields
    )
    @users_api.response(HTTPStatus.BAD_REQUEST, description='Error', model=error_fields)
    @users_api.expect(currency_input_fields)
    def post(self, user_id: str) -> Any:
        try:
            validated_json = validate_request_json(request.data, currency_input_fields)
            user_id_in_int = validate_path_parameter(user_id)

        except (ValidationException, UsersDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST

        # ошибка будет при неправильном id пользоватлей или валюты,
        # при неправильном времени(больше текущего),
        # при ошибке при покупке, продаже(-баланс), при изменении курса


@users_api.route('/<user_id>/operations/')
@users_api.param('user_id', 'User id')
@users_api.param('operation_type', 'History by type of operation')
@users_api.param('size', 'Pagination page size')
@users_api.param('page', 'Pagination page')
class UserOperations(Resource):
    @users_api.marshal_list_with(operation_fields, code=HTTPStatus.OK)
    @users_api.response(HTTPStatus.BAD_REQUEST, 'Error', model=error_fields)
    def get(self, user_id: str) -> Any:
        try:
            validated_params: Dict[str, Any] = validate_request_params(
                dict(user_id=int, operation_type=OperationType, size=int, page=int),
                request.values)
            user_id_in_int = validate_path_parameter(user_id)
        except ValidationException:
            pass

    # ошибка, если пользователь указан неверно, неправильно заданы параметры пагинации,
    # operation_type is invalid
