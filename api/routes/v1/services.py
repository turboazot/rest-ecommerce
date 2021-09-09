import flask
import flask_restx
import http
import api.repositories.service as service_repository
from api.schemas.service import ServiceSchema
from api.helpers.response_list import ResponseList
from api.helpers.response_single import ResponseSingle
from api.helpers.response_ok import ResponseOK

services_ns = flask_restx.Namespace('services',
                                    description='Services in platform')


@services_ns.route('/')
class Services(flask_restx.Resource):
    @staticmethod
    def get():
        page = int(flask.request.args.get('page', 1))
        per_page = int(flask.request.args.get('per-page', 10))

        services = service_repository.get_all(page, per_page)

        return ResponseList(services, ServiceSchema()).render()
    
    @staticmethod
    def post():
        data = flask.request.get_json()
        service = service_repository.create(data)
        return ResponseSingle(service, ServiceSchema()).render()

@services_ns.route('/<id>')
class ServiceSingle(flask_restx.Resource):
    @staticmethod
    def get(id):
        service = service_repository.get_one(id)
        return ResponseSingle(service, ServiceSchema()).render()
    
    @staticmethod
    def patch(id):
        data = flask.request.get_json()
        service = service_repository.update(id, data)
        return ResponseSingle(service, ServiceSchema()).render()
    
    @staticmethod
    def delete(id):
        service_repository.delete(id)
        return ResponseOK().render()


