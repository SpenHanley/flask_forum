from utils import Config as config
import os
import random
import string


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

class Config(object):
    """
    Common configuration options
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/fforum_db'
    SECRET_KEY = load_secret_key()
    SECURITY_PASSWORD_SALT = 'q+s|cP2Mr);ScNL;nXJa?Rw:Ji|JSlC&hXd2/wGG,6mh?4o8-K=_yV88g>eR/j:O'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True

    # We need to load the configuration before we can use it
    conf = config()

    conf.load_config()
    
    # Mail configuration
    MAIL_SERVER   = conf.get('mail_server')
    MAIL_TLS_PORT = conf.get('mail_tls_port')
    MAIL_SSL_PORT = conf.get('mail_ssl_port')
    MAIL_USE_TLS  = conf.get('mail_use_tls')
    MAIL_USE_SSL  = conf.get('mail_use_ssl')

    # Mail authentication
    MAIL_USERNAME = config.get('mail_username')
    MAIL_PASSWORD = config.get('mail_password')
    MAIL_SENDER   = config.get('mail_sender_address')


class DevelopmentConfig(Config):
    """
    Development configuration options
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
    Production config
    """
    DEBUG = False
    SQLALCHEMY_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
