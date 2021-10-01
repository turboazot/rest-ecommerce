from api.extensions import db
from sqlalchemy.orm import relationship


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column('id', db.Integer, primary_key=True)
    quantity = db.Column('quantity', db.Integer, nullable=False)

    order_id = db.Column('order_id', db.Integer, db.ForeignKey('orders.id'))
    order = relationship("Order", back_populates="order_items")

    product_id = db.Column("product_id", db.Integer, db.ForeignKey('products.id'))
    product = relationship("Product")

    def __repr__(self):
        return f'<OrderItem "{self.id}">'
