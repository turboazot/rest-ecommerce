from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.models.user import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True