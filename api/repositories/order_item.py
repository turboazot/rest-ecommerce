from api.extensions import db
from api.models.order_item import OrderItem
from api.models.order import Order
from api.models.product import Product
import uuid


def get_all(order_id):
    return OrderItem.query.filter_by(order_id=order_id).all()

def create(order_id, data):
    order_item = OrderItem()
    order_item_id = str(uuid.uuid4())
    order_item.id = {
        "id": order_item_id,
        "partition_key": order_id
    }
    order_item.quantity = int(data["quantity"])

    order = Order.query.get_or_404({
        "id": order_id,
        "partition_key": order_id
    })
    product = Product.query.get_or_404(data["product_id"])

    order_item.order_id = order.id
    order_item.order = order
    order_item.product_id = product.id
    order_item.product = product

    db.session.add(order_item)
    db.session.commit()
    db.session.close()
    db.default_session.close()

    return order_item

def get_one(order_id, id):
    result = OrderItem.query.get_or_404({
        "id": id,
        "partition_key": order_id
    })
    db.session.close()
    return result


def update(order_id, id, data):
    order_item = OrderItem.query.get_or_404({
        "id": id,
        "partition_key": order_id
    })
    
    order_item.quantity = int(data["quantity"])

    db.session.commit()
    db.session.close()

    return order_item

def delete(order_id, id):
    order_item = OrderItem.query.get_or_404({
        "id": id,
        "partition_key": order_id
    })
    OrderItem.query.filter_by(id={
        "id": id,
        "partition_key": order_id
    }).delete()
    db.session.commit()
    db.session.close()
