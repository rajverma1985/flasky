import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something_Really_difficult_too_guess'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get("MAIL_USER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@razz.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URL') or "postgresql://raj:test@localhost/flasky_dev"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB_URL') or "postgresql://raj:test@localhost/flasky_prod"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL') or "sqlite://"


config = {'development': DevelopmentConfig,
          'testing': TestConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
          }
