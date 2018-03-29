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

def load_salt():
    if not os.path.isfile('security.key'):
        s = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(64))
        with open('security.key', 'w') as key:
            key.write(s)
    else:
        with open('security.key', 'r') as key:
            s = key.read()
    return s



def create_upload_folder():
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')


class Config(object):
    """
    Common configuration options
    """
    # Need to find a way to generate this similar to the application salt
    SECURITY_PASSWORD_SALT = load_salt()
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
    MAIL_USERNAME = conf.get('mail_username')
    MAIL_PASSWORD = conf.get('mail_password')
    MAIL_SENDER = conf.get('mail_sender_address')

    POSTGRES_USERNAME = conf.get('postgres_username')
    POSTGRES_PASSWORD = conf.get('postgres_password')

    UPLOAD_FOLDER = 'uploads'

    SQLALCHEMY_DATABASE_URI = 'postgres//{}:{}@localhost/flask_db'.format(POSTGRES_USERNAME, POSTGRES_PASSWORD)
    SECRET_KEY = load_secret_key()


class DevelopmentConfig(Config):
    """
    Development configuration options
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
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
