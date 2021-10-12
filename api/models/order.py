from api.extensions import db
from sqlalchemy.orm import relationship
from api.extensions import BindKeyPattern

class Order(db.Model):
    __tablename__ = 'orders'
    __bind_key__ = BindKeyPattern(r'order_\d+')

    id = db.Column('id', db.String(36), primary_key=True)
    status = db.Column('status', db.String(50), nullable=False)

    user_id = db.Column('user_id', db.String(36))

    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f'<Order "{self.id}">'
