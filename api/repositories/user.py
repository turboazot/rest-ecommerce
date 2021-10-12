from api.extensions import db
from api.models.user import User
import uuid


def get_all(page, per_page):
    result = User.query.paginate(page, per_page)
    db.default_session.close()
    return result

def create(data):
    user = User()
    user.id = uuid.uuid4()
    user.username = data["username"]

    db.default_session.add(user)
    db.default_session.commit()
    db.default_session.close()
    return user

def get_one(id):
    result = User.query.get_or_404(id)
    db.default_session.close()
    return result


def update(id, data):
    user = User.query.get_or_404(id)
    
    user.username = data["username"]

    db.default_session.commit()
    db.default_session.close()

    return user

def delete(id):
    user = User.query.get_or_404(id)
    db.default_session.delete(user)
    db.default_session.commit()
    db.default_session.close()

