from api.extensions import db
from sqlalchemy.orm import relationship

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column('id', db.Integer, primary_key=True)
    status = db.Column('status', db.String(50), nullable=False)

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f'<Order "{self.id}">'
