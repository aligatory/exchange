from http import HTTPStatus
from typing import Any

from exchange.api.root_controller import error_fields
from exchange.custom_fields import Decimal, String
from exchange.dal.currencies_dal import CurrenciesDAL
from exchange.exceptions import CurrenciesDALException, ValidationException
from exchange.validation import validate_path_parameter, validate_request_json
from flask import request
from flask_restplus import Namespace, Resource, abort, fields, marshal

currencies_api: Namespace = Namespace('currencies', description='Currencies operations')

currencies_input_fields = currencies_api.model(
    'CurrencyInput',
    {
        'name': String(requiered=True),
        'purchasing_price': Decimal(required=True),
        'selling_price': Decimal(required=True),
    },
)

currency_output_fields = currencies_api.model(
    'Currency',
    {
        'name': fields.String,
        'purchasing_price': fields.Fixed,
        'selling_price': fields.Fixed,
        'time': fields.String,
        'id': fields.Integer,
    },
)

currency_history_output_fields = currencies_api.model(
    'CurrencyHistory',
    {
        'purchasing_price': fields.Fixed,
        'selling_price': fields.Fixed,
        'time': fields.String,
    },
)


@currencies_api.route('/')
class Currencies(Resource):
    @currencies_api.marshal_list_with(currency_output_fields, code=HTTPStatus.OK)
    def get(self) -> Any:
        return CurrenciesDAL.get_currencies()

    @currencies_api.expect(currencies_input_fields, code=HTTPStatus.CREATED)
    @currencies_api.response(
        HTTPStatus.BAD_REQUEST, description='Error', model=error_fields
    )
    @currencies_api.response(
        description='Currency added',
        model=currency_output_fields,
        code=HTTPStatus.CREATED,
    )
    def post(self) -> Any:
        try:
            validated_json = validate_request_json(
                request.data, currencies_input_fields
            )
            return (
                marshal(
                    CurrenciesDAL.add_currency(**validated_json),
                    currency_output_fields,
                ),
                HTTPStatus.CREATED,
            )
        except (ValidationException, CurrenciesDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST


@currencies_api.route('/<currency_id>/')
@currencies_api.param('currency_id', 'Currency id')
class Currency(Resource):
    @currencies_api.response(
        HTTPStatus.OK, description='OK', model=currency_output_fields
    )
    @currencies_api.response(
        HTTPStatus.BAD_REQUEST, description='Error', model=error_fields
    )
    def get(self, currency_id: str) -> Any:
        request.get_json()
        try:
            currency_id_in_int: int = validate_path_parameter(currency_id)
            return (
                marshal(
                    CurrenciesDAL.get_currency_by_id(currency_id_in_int),
                    currency_output_fields,
                ),
                HTTPStatus.OK,
            )
        except (ValidationException, CurrenciesDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST


@currencies_api.route('/<currency_id>/history/')
@currencies_api.param('currency_id', 'Currency id')
class CurrencyHistory(Resource):
    @currencies_api.marshal_list_with(currency_history_output_fields)
    def get(self, currency_id: str):  # type: ignore
        try:
            currency_id_in_int: int = validate_path_parameter(currency_id)
            return CurrenciesDAL.get_currency_history(currency_id_in_int)
        except (ValidationException, CurrenciesDALException) as e:
            abort(HTTPStatus.BAD_REQUEST, e)
