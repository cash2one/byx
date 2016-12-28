# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main.login'
login_manager.login_message = u""


def create_app(config_name):
    app = Flask(__name__)
    app.jinja_env.globals['ART_TYPE_LIST'] = {0: u'珂罗版', 1: u'丝网版', 2: u'木版', 3: u'铜版', 4: u'石版', 5: u'综合版',
                                              6: u'艺术微喷', 7: u'艺术衍生品', 8: u'艺术走进生活', 99: u'其他'}
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
