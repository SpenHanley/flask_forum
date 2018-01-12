from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

from config import app_config

app = Flask(__name__, instance_relative_config=True)
mail = Mail(app)
login_manager = LoginManager()


def create_app(config_name):
    global db
    app = Flask(__name__, instance_relative_config=True)
    sslify = SSLify(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/fforum_db'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db = SQLAlchemy(app)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .registered_user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
