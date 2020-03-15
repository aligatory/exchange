from flask_restplus import Api

from .currencies_controller import currencies_api
from .root_controller import root_api
from .users_controller import users_api

api = Api(doc='/api')
api.add_namespace(currencies_api, path='/currencies')
api.add_namespace(users_api, path='/users')
api.add_namespace(root_api)
