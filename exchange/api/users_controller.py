from http import HTTPStatus
from typing import Any

from exchange.api.custom_fields import String
from exchange.api.root_controller import error_fields
from exchange.api.validation import get_dict_from_json, validate_json, validate_path_parameter
from exchange.dal.users_dal import UsersDAL
from exchange.exceptions import UsersDALException, ValidationException
from flask import request
from flask_restplus import Namespace, Resource, fields, marshal

users_api: Namespace = Namespace('users', description='Users related operations')

user_input_fields = users_api.model('User', {'login': String(required=True)})

user_output_fields = users_api.inherit(
    'UserInput', user_input_fields, {'money': fields.String}
)

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

currency_operation_fields = users_api.model(
    'Currencies operation',
    {
        'currency_id': fields.Integer,
        'operation_type': fields.String,
        'amount': fields.Float,
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
            input_json = get_dict_from_json(request.data)
            validate_json(input_json, user_input_fields)
            return (
                marshal(
                    UsersDAL.add_user(self.api.payload['login']), user_output_fields
                ),
                HTTPStatus.CREATED,
            )
        except (ValidationException, UsersDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST


@users_api.route('/<user_id>/currencies/')
@users_api.param('user_id', 'User id')
class UserCurrencies(Resource):
    @users_api.response(HTTPStatus.BAD_REQUEST, description='error', model=error_fields)
    @users_api.marshal_list_with(currency_fields, code=HTTPStatus.OK)
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
        HTTPStatus.CREATED, description='Operation done', model=currency_fields
    )
    @users_api.response(HTTPStatus.BAD_REQUEST, description='Error', model=error_fields)
    @users_api.expect(currency_operation_fields)
    def post(self, user_id: str) -> Any:
        input_json = request.json
        validate_url_params
        validate_json(input_json, currency_fields)
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
        user_id_in_int = validate_path_parameter(user_id)
        # ошибка, если пользователь указан неверно, неправильно заданы параметры пагинации,
        # operation_type is invalid
        pass
