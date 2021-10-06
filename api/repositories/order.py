from api.extensions import db
from api.models.order import Order
from api.models.user import User
import http
from flask import abort


def get_all(user_id, page, per_page):
    return Order.query.filter_by(user_id=user_id).paginate(page, per_page)

def create(user_id, data):
    order = Order()
    user = User.query.get_or_404(user_id)

    order.user = user
    order.status = "pending"

    db.session.add(order)
    db.session.commit()
    return order

def get_one(id):
    return Order.query.get_or_404(id)


def update(id, data):
    order = Order.query.get_or_404(id)
    
    order.status = data["status"]

    db.session.commit()

    return order

def delete(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
