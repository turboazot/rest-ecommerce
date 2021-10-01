from api.extensions import db
from api.models.order_item import OrderItem
from api.models.order import Order
from api.models.product import Product


def get_all(order_id, page, per_page):
    return OrderItem.query.filter_by(order_id=order_id).paginate(page, per_page)

def create(order_id, data):
    order_item = OrderItem()
    order_item.quantity = int(data["quantity"])

    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(int(data["product_id"]))
    order_item.order = order
    order_item.product = product

    db.session.add(order_item)
    db.session.commit()
    return order_item

def get_one(id):
    return OrderItem.query.get_or_404(id)


def update(id, data):
    order_item = OrderItem.query.get_or_404(id)
    
    order_item.quantity = int(data["quantity"])

    db.session.commit()

    return order_item

def delete(id):
    order_item = OrderItem.query.get_or_404(id)
    db.session.delete(order_item)
    db.session.commit()
