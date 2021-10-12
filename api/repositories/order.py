from api.extensions import db
from api.models.order import Order
from api.models.order_item import OrderItem
from api.models.user import User
import http
from flask import abort
import uuid


def get_all(user_id):
    result = Order.query.filter_by(user_id=user_id).all()
    db.session.close()
    return result

def create(user_id, data):
    order = Order()
    order_id = uuid.uuid4()
    order.id = {
        "id": order_id,
        "partition_key": order_id
    }
    user = User.query.get_or_404(user_id)

    order.user_id = user.id
    order.status = "pending"

    db.session.add(order)
    db.session.commit()
    order.order_items = OrderItem.query.filter_by(order_id=order.id).all()
    db.default_session.close()
    db.session.close()


    return order

def get_one(id):
    result = Order.query.get_or_404({
        "id": id,
        "partition_key": id
    })
    db.session.close()

    return result


def update(id, data):
    order = Order.query.get_or_404({
        "id": id,
        "partition_key": id
    })
    order.status = data["status"]

    db.session.commit()
    db.session.close()

    return order

def delete(id):
    order = Order.query.get_or_404({
        "id": id,
        "partition_key": id
    })
    Order.query.filter_by(id={
        "id": id,
        "partition_key": id
    }).delete()
    db.session.commit()
    db.session.close()
