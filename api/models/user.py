from api.extensions import db
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(127), unique=True)

    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f'<User "{self.id}">'
