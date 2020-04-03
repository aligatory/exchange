from flask_restplus import Namespace, fields

root_api = Namespace('root', description='root')

error_fields = root_api.model('Error', {'message': fields.String})
