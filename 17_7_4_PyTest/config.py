import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    DEBUG = True
    TESTING = True