from api.extensions import db
from api.models.user import User


def get_all(page, per_page):
    return User.query.paginate(page, per_page)

def create(data):
    user = User()
    user.username = data["username"]

    db.session.add(user)
    db.session.commit()
    return user

def get_one(id):
    return User.query.get_or_404(id)


def update(id, data):
    user = User.query.get_or_404(id)
    
    user.username = data["username"]

    db.session.commit()

    return user

def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
