from api.extensions import db
from api.models.product import Product


def get_all(page, per_page):
    return Product.query.paginate(page, per_page)

def create(data):
    product = Product()
    product.name = data["name"]
    product.price = float(data["price"])

    db.session.add(product)
    db.session.commit()
    return product

def get_one(id):
    return Product.query.get_or_404(id)


def update(id, data):
    product = Product.query.get_or_404(id)
    
    product.name = data["name"]
    product.price = float(data["price"])

    db.session.commit()

    return product

def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
