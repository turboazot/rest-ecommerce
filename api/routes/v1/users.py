import flask
import flask_restx
import http
from api.schemas.user import UserSchema
from api.schemas.order import OrderSchema
from api.schemas.order_item import OrderItemSchema
from api.helpers.response_list import ResponseList
from api.helpers.response_single import ResponseSingle
from api.helpers.response_ok import ResponseOK
import api.repositories.user as user_repository
import api.repositories.order as order_repository
import api.repositories.order_item as order_item_repository

users_ns = flask_restx.Namespace('users',
                                    description='Users in platform')


@users_ns.route('/')
class Users(flask_restx.Resource):
    @staticmethod
    def get():
        page = int(flask.request.args.get('page', 1))
        per_page = int(flask.request.args.get('per-page', 10))

        users = user_repository.get_all(page, per_page)

        return ResponseList(users, UserSchema()).render()
    
    @staticmethod
    def post():
        data = flask.request.get_json()
        user = user_repository.create(data)
        return ResponseSingle(user, UserSchema()).render()

@users_ns.route('/<id>')
class UserSingle(flask_restx.Resource):
    @staticmethod
    def get(id):
        user = user_repository.get_one(id)
        return ResponseSingle(user, UserSchema()).render()
    
    @staticmethod
    def patch(id):
        data = flask.request.get_json()
        user = user_repository.update(id, data)
        return ResponseSingle(user, UserSchema()).render()
    
    @staticmethod
    def delete(id):
        user_repository.delete(id)
        return ResponseOK().render()

@users_ns.route('/<user_id>/orders')
class Orders(flask_restx.Resource):
    @staticmethod
    def get(user_id):
        page = int(flask.request.args.get('page', 1))
        per_page = int(flask.request.args.get('per-page', 10))

        orders = order_repository.get_all(user_id, page, per_page)

        return ResponseList(orders, OrderSchema()).render()
    
    @staticmethod
    def post(user_id):
        data = flask.request.get_json()
        order = order_repository.create(user_id, data)
        return ResponseSingle(order, OrderSchema()).render()

@users_ns.route('/<user_id>/orders/<order_id>')
class OrderSingle(flask_restx.Resource):
    @staticmethod
    def get(user_id, order_id):
        order = order_repository.get_one(order_id)
        return ResponseSingle(order, OrderSchema()).render()
    
    @staticmethod
    def patch(user_id, order_id):
        data = flask.request.get_json()
        order = order_repository.update(order_id, data)
        return ResponseSingle(order, OrderSchema()).render()
    
    @staticmethod
    def delete(user_id, order_id):
        order_repository.delete(order_id)
        return ResponseOK().render()

@users_ns.route('/<user_id>/orders/<order_id>/order-items')
class OrderItemLists(flask_restx.Resource):
    @staticmethod
    def get(user_id, order_id):
        page = int(flask.request.args.get('page', 1))
        per_page = int(flask.request.args.get('per-page', 10))

        order_items = order_item_repository.get_all(order_id, page, per_page)

        return ResponseList(order_items, OrderItemSchema()).render()
    
    @staticmethod
    def post(user_id, order_id):
        data = flask.request.get_json()
        order_item = order_item_repository.create(order_id, data)
        return ResponseSingle(order_item, OrderItemSchema()).render()


@users_ns.route('/<user_id>/orders/<order_id>/order-items/<order_item_id>')
class OrderItemSingle(flask_restx.Resource):
    @staticmethod
    def get(user_id, order_id, order_item_id):
        order_item = order_item_repository.get_one(order_item_id)
        return ResponseSingle(order_item, OrderItemSchema()).render()
    
    @staticmethod
    def patch(user_id, order_id, order_item_id):
        data = flask.request.get_json()
        order_item = order_item_repository.update(order_item_id, data)
        return ResponseSingle(order_item, OrderItemSchema()).render()
    
    @staticmethod
    def delete(user_id, order_id, order_item_id):
        order_item_repository.delete(order_item_id)
        return ResponseOK().render()
