import os


class DefaultConfig(object):
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    V1_PREFIX = '/api/v1'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


PROFILE = os.environ.get('PROFILE', 'default')
config_class = f'{PROFILE.title()}Config'

Config = globals()[config_class]
