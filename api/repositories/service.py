from api.models.service import Service
from api.extensions import db

def create(data):
    service = Service(**data)
    db.session.add(service)
    db.session.commit()
    return service

def get_one(id):
    return Service.query.get_or_404(id)

def get_all(page=1, per_page=2):
    return Service.query.paginate(page, per_page, error_out=False)

def update(id, data):
    service = Service.query.get_or_404(id)
    service.name = data['name']
    service.description = data['description']

    db.session.commit()
    return service

def delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()