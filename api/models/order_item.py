from api.extensions import db
from sqlalchemy.orm import relationship
from api.extensions import BindKeyPattern

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    __bind_key__ = BindKeyPattern(r'order_\d+')

    id = db.Column('id', db.String(36), primary_key=True)
    quantity = db.Column('quantity', db.Integer, nullable=False)

    order_id = db.Column('order_id', db.String(36), db.ForeignKey('orders.id'))
    order = relationship("Order", back_populates="order_items")

    product_id = db.Column("product_id", db.String(36), nullable=False)

    def __repr__(self):
        return f'<OrderItem "{self.id}">'
