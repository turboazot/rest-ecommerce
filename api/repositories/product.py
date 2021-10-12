from api.extensions import db
from api.models.product import Product
import uuid


def get_all(page, per_page):
    result = Product.query.paginate(page, per_page)
    db.default_session.close()
    
    return result

def create(data):
    product = Product()
    product.id = uuid.uuid4()
    product.name = data["name"]
    product.price = float(data["price"])

    db.default_session.add(product)
    db.default_session.commit()
    db.default_session.close()

    return product

def get_one(id):
    result = Product.query.get_or_404(id)
    db.default_session.close()
    return result


def update(id, data):
    product = Product.query.get_or_404(id)
    
    product.name = data["name"]
    product.price = float(data["price"])

    db.default_session.commit()
    db.default_session.close()


    return product

def delete(id):
    product = Product.query.get_or_404(id)
    db.default_session.delete(product)
    db.default_session.commit()
    db.default_session.close()

