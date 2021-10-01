from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from api.models.order_item import OrderItem
from api.schemas.product import ProductSchema

class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        load_instance = True
    
    product = fields.Nested(ProductSchema)