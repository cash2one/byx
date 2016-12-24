import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'

    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1@127.0.0.1/spider'
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/upload')


config = {
    'default': DevelopConfig,
}