from api.extensions import db


class Service(db.Model):
    __tablename__ = 'services'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(127))
    description = db.Column('description', db.String(1024))

    def __repr__(self):
        return f'<Service "{self.id}">'
