from http import HTTPStatus
from typing import Optional

from flask_restplus import Namespace, Resource, fields

from .root_controller import error_fields

currencies_api: Namespace = Namespace('currencies', description='Currencies operations')

currency_fields_for_adding = currencies_api.model(
    'Currency1',
    {
        'name': fields.String,
        'purchasing_price': fields.Float,
        'selling_price': fields.Float,
    },
)

currency_fields = currencies_api.inherit(
    'Currency', currency_fields_for_adding, {'time': fields.DateTime}
)


@currencies_api.route('/')
class Currencies(Resource):
    @currencies_api.marshal_list_with(currency_fields, code=HTTPStatus.OK)
    def get(self):
        pass

    @currencies_api.expect(currency_fields_for_adding, code=HTTPStatus.CREATED)
    @currencies_api.response(HTTPStatus.BAD_REQUEST, description="Error", model=error_fields)
    def post(self):
        # ошибка при валидации json
        pass


@currencies_api.route('/<currency_id>/')
@currencies_api.param('currency_id', 'Currency id')
class Currency(Resource):
    @currencies_api.marshal_with(currency_fields, code=HTTPStatus.OK)
    @currencies_api.response(
        HTTPStatus.BAD_REQUEST, description='Error', model=error_fields
    )
    def get(self, currency_id: str):
        # ошибка падает, если такой валюты не сущ
        pass
