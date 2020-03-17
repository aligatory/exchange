from http import HTTPStatus

from exchange.api.custom_fields import Decimal, String
from exchange.api.root_controller import error_fields
from exchange.api.validation import get_dict_from_json, validate_json
from exchange.dal.currencies_dal import CurrenciesDAL
from exchange.exceptions import CurrenciesDALException, ValidationException
from flask import request
from flask_restplus import Namespace, Resource, fields, marshal

currencies_api: Namespace = Namespace('currencies', description='Currencies operations')

currencies_input_fields = currencies_api.model(
    'CurrencyInput',
    {
        'name': String(requiered=True),
        'purchasing_price': Decimal(True),
        'selling_price': Decimal(True),
    },
)

currency_output_fields = currencies_api.inherit(
    'Currency', currencies_input_fields, {'time': fields.DateTime, 'id': fields.Integer}
)


@currencies_api.route('/')
class Currencies(Resource):
    @currencies_api.marshal_list_with(currency_output_fields, code=HTTPStatus.OK)
    def get(self):
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
    def post(self):
        try:
            input_json = get_dict_from_json(request.data)
            validate_json(input_json, currencies_input_fields)
<<<<<<< HEAD
            return (
                marshal(
                    CurrenciesDAL.add_currency(**input_json), currency_output_fields,
                ),
                HTTPStatus.CREATED,
            )
=======
            return marshal(
                CurrenciesDAL.add_currency(**input_json),
                currency_output_fields,
            ), HTTPStatus.CREATED
>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
        except (ValidationException, CurrenciesDALException) as e:
            return marshal({'message': e}, error_fields), HTTPStatus.BAD_REQUEST


@currencies_api.route('/<currency_id>/')
@currencies_api.param('currency_id', 'Currency id')
class Currency(Resource):
    # @currencies_api.marshal_with(currency_output_fields, code=HTTPStatus.OK)
    @currencies_api.response(
        HTTPStatus.BAD_REQUEST, description='Error', model=error_fields
    )
    def get(self, currency_id: str):
        # ошибка падает, если такой валюты не сущ
        pass
