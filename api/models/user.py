from api.extensions import db
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'users'
    query = db.default_session.query_property()

    id = db.Column('id', db.String(36), primary_key=True)
    username = db.Column('username', db.String(127), unique=True)

    def __repr__(self):
        return f'<User "{self.id}">'
