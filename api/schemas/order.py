from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.models.order import Order

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True