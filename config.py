import os
import random
import string

from utils import Config as config


def load_secret_key():
    if not os.path.isfile('secret.key'):
        s = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(64))
        with open('secret.key', 'w') as key:
            key.write(s)
    else:
        with open('secret.key', 'r') as key:
            s = key.read()
    return s


def create_upload_folder():
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')


class Config(object):
    """
    Common configuration options
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/forum_db'
    SECRET_KEY = load_secret_key()
    # Need to find a way to generate this similar to the application salt
    SECURITY_PASSWORD_SALT = 'q+s|cP2Mr);ScNL;nXJa?Rw:Ji|JSlC&hXd2/wGG,6mh?4o8-K=_yV88g>eR/j:O'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True

    # We need to load the configuration before we can use it
    conf = config()

    conf.load_config()

    # Mail configuration
    MAIL_SERVER = conf.get('mail_server')
    MAIL_TLS_PORT = conf.get('mail_tls_port')
    MAIL_SSL_PORT = conf.get('mail_ssl_port')
    MAIL_USE_TLS = conf.get('mail_use_tls')
    MAIL_USE_SSL = conf.get('mail_use_ssl')

    # Mail authentication
    MAIL_USERNAME = config.get('mail_username')
    MAIL_PASSWORD = config.get('mail_password')
    MAIL_SENDER = config.get('mail_sender_address')

    UPLOAD_FOLDER = 'uploads'


class DevelopmentConfig(Config):
    """
    Development configuration options
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/forum_db'
    DEBUG = True


class ProductionConfig(Config):
    """
    Production config
    """
    DEBUG = False
    SQLALCHEMY_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This will be the base uploads directory, it will have subdirectories
    # for profiles, posts, forums and others to suit.
    UPLOAD_FOLDER = 'uploads'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
