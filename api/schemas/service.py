from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.models.service import Service

class ServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = True