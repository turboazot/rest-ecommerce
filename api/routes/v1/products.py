import flask
import flask_restx
import http
from api.schemas.product import ProductSchema
from api.helpers.response_pagination import ResponsePagination
from api.helpers.response_single import ResponseSingle
from api.helpers.response_ok import ResponseOK
import api.repositories.product as product_repository

products_ns = flask_restx.Namespace('products',
                                    description='Products in platform')


@products_ns.route('/')
class Products(flask_restx.Resource):
    @staticmethod
    def get():
        page = int(flask.request.args.get('page', 1))
        per_page = int(flask.request.args.get('per-page', 10))

        products = product_repository.get_all(page, per_page)

        return ResponsePagination(products, ProductSchema()).render()
    
    @staticmethod
    def post():
        data = flask.request.get_json()
        product = product_repository.create(data)
        return ResponseSingle(product, ProductSchema()).render()

@products_ns.route('/<id>')
class ProductSingle(flask_restx.Resource):
    @staticmethod
    def get(id):
        product = product_repository.get_one(id)
        return ResponseSingle(product, ProductSchema()).render()
    
    @staticmethod
    def patch(id):
        data = flask.request.get_json()
        product = product_repository.update(id, data)
        return ResponseSingle(product, ProductSchema()).render()
    
    @staticmethod
    def delete(id):
        product_repository.delete(id)
        return ResponseOK().render()
