from api import models
import api.app
import flask
import api.extensions
import click
from faker import Faker
import api.repositories.user as user_repository
import api.repositories.product as product_repository

app = api.app.create_app()


@app.cli.command('migrate')
def migrate():
    api.extensions.db.create_all()


@app.cli.command('seed')
@click.option("-uc", "--users-count", default=10)
@click.option("-pc", "--products-count", default=10)
def seed(users_count, products_count):
    fake = Faker()

    print("========== USER CREATION ==========")
    for _ in range(users_count):
        user = user_repository.create({
            "username": fake.name() + " " + fake.pystr(max_chars=3)
        })
        print(user)
    
    print("========== PRODUCTS CREATION ==========")
    for _ in range(products_count):
        product = product_repository.create({
            "name": fake.company() + " " + fake.pystr(max_chars=3),
            "price": fake.pyfloat(positive=True)
        })
        print(product)
