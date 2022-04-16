import os
from dotenv import load_dotenv

load_dotenv()


def get_env_db_url(env_setting):
    if env_setting == "dev":
        path = os.environ.get("SQLALCHEMY_DATABASE_URI")
    elif env_setting == "testing":
        path = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    return str(path)


TEST_DB_URL = get_env_db_url('testing')
DEV_DB_URL = get_env_db_url('dev')


class Config(object):
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TEST_DB_URL
    DEBUG = True
    TESTING = True

