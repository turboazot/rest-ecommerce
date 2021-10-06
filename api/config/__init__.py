import os


class DefaultConfig(object):
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    V1_PREFIX = '/api/v1'
    DEBUG = True

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_NAME = 'rest'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


PROFILE = os.environ.get('PROFILE', 'default')
config_class = f'{PROFILE.title()}Config'

Config = globals()[config_class]
