import os

class DefaultConfig(object):
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    V1_PREFIX = '/api/v1'
    DEBUG = True

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_NAME = 'rest'
    ORDER_DB_USERNAME = os.getenv("ORDER_DB_USERNAME", "order")
    ORDER_DB_PASSWORD = os.getenv("ORDER_DB_PASSWORD", "order")
    ORDER_DB_NAME = 'order'
    ORDER_DB_HOSTS = os.getenv("ORDER_DB_HOSTS", "127.0.0.1:3307,127.0.0.1:3308")
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


PROFILE = os.environ.get('PROFILE', 'default')
config_class = f'{PROFILE.title()}Config'

Config = globals()[config_class]
Config.SQLALCHEMY_BINDS = {}

order_hosts = Config.ORDER_DB_HOSTS.split(",")

for order_host_number in range(0, len(order_hosts)):
    Config.SQLALCHEMY_BINDS[f"order_{order_host_number}"] = 'mysql://{}:{}@{}/{}'.format(Config.ORDER_DB_USERNAME, Config.ORDER_DB_PASSWORD, order_hosts[order_host_number], Config.ORDER_DB_NAME)
