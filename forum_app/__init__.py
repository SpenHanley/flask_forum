from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from site_nav import configure_nav
from config import app_config

app = Flask(__name__, instance_relative_config=True)
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    # app_config is part of another python file that I need to recreate
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to view this page'
    login_manager.login_view = 'security.login'

    configure_nav(app)

    from . import models

    from _admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from _security import security as security_blueprint
    app.register_blueprint(security_blueprint)

    from _home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
