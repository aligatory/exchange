from http import HTTPStatus
from typing import Any, Dict

from exchange.api.root_controller import error_fields
from exchange.custom_fields import DateTime, Decimal, Integer
from exchange.custom_fields import OperationType as OTField
from exchange.custom_fields import String
from exchange.dal.users_dal import UsersDAL
from exchange.exceptions import PaginationError, UsersDALException, ValidationException
from exchange.operation_type import OperationType
from exchange.validation import (
    RequestParam,
    validate_path_parameter,
    validate_request_json,
    validate_request_params,
)
from flask import request
from flask_restplus import Namespace, Resource, abort, fields, marshal

users_api: Namespace = Namespace('users', description='Users related operations')

user_input_fields = users_api.model('User', {'login': String(required=True)})

user_output_fields = users_api.inherit(
    'UserInput', user_input_fields, {'id': fields.Integer,'money': fields.Fixed}
)

currency_output_fields = users_api.model(
    'Currencies',
    {
        'id': fields.Integer,
        'currency_id': fields.Integer,
        'user_id': fields.Integer,
        'amount': fields.Fixed,
    },
)

currency_input_fields = users_api.model(
    'InputCurrencies',
    {
        'currency_id': Integer(required=True),
        'operation': OTField(required=True),
        'amount': Decimal(required=True),
        'time': DateTime(required=True),
    },
)
operation_fields = users_api.model(
    'Operation',
    {
        'id': fields.Integer,
        'operation_type': fields.String,
        'currency_id': fields.Integer,
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
                marshal(UsersDAL.add_user(validated_json['login']), user_output_fields),
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
        try:
            user_id_int = validate_path_parameter(user_id)
            return UsersDAL.get_user_currencies(user_id_int)
        except (UsersDALException, ValidationException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST

    @users_api.response(
        HTTPStatus.CREATED, description='Operation done', model=currency_output_fields
    )
    @users_api.response(HTTPStatus.BAD_REQUEST, description='Error', model=error_fields)
    @users_api.expect(currency_input_fields)
    def post(self, user_id: str) -> Any:
        try:
            validated_json = validate_request_json(request.data, currency_input_fields)
            user_id_in_int = validate_path_parameter(user_id)
            return (
                marshal(
                    UsersDAL.make_operation_with_currency(
                        user_id_in_int, **validated_json
                    ),
                    currency_output_fields,
                ),
                HTTPStatus.CREATED,
            )
        except (ValidationException, UsersDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST


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
            validated_params: Dict[str, RequestParam] = validate_request_params(
                dict(
                    operation_type=RequestParam(OperationType),
                    size=RequestParam(int),
                    page=RequestParam(int),
                ),
                request.values,
            )
            user_id_in_int = validate_path_parameter(user_id)
            return UsersDAL.get_user_operations_history(
                user_id_in_int, **validated_params  # type: ignore
            )
        except (ValidationException, PaginationError, UsersDALException) as e:
            abort(HTTPStatus.BAD_REQUEST, e)


@users_api.route('/<user_id>/')
@users_api.param('user_id', 'User id')
@users_api.response(HTTPStatus.OK, description='Success', model=user_output_fields)
@users_api.response(HTTPStatus.BAD_REQUEST, description='Error', model=error_fields)
class UserMoney(Resource):
    def get(self, user_id: str) -> Any:
        try:
            user_id_in_int = validate_path_parameter(user_id)
            return (
                marshal(UsersDAL.get_user(user_id_in_int), user_output_fields),
                HTTPStatus.OK,
            )
        except (ValidationException, UsersDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST
