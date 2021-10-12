from api.extensions import db


class Product(db.Model):
    __tablename__ = 'products'
    query = db.default_session.query_property()

    id = db.Column('id', db.String(36), primary_key=True)
    name = db.Column('name', db.String(127), unique=True)
    price = db.Column('price', db.Float)

    def __repr__(self):
        return f'<Product "{self.id}">'
