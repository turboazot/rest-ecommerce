from api.extensions import db


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(127), unique=True)
    price = db.Column('price', db.Float)

    def __repr__(self):
        return f'<Product "{self.id}">'
