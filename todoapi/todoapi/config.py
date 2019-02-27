import os


class BaseConfig:
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_BLACKLIST_ENABLED = True
	JWT_BLACKLIST_TOKEN_CHECKS = ['access']


class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	JWT_SECRET_KEY = 'dev-jwt-top-secret-key'


class TestingConfig(BaseConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
	PRESERVE_CONTEXT_ON_EXCEPTION = False
