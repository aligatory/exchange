from flask_restplus import Namespace, Resource, fields

root_api = Namespace('root', description='root')
error_fields = root_api.model('Error', {'message': fields.String})


@root_api.route('/')
class Index(Resource):
    def index(self) -> str:
        return 'покупаем, докупаем, фиксируем прибыль'
