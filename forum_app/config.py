from utils import generate, load_security_file


class Config(object):
    """
    The base configuration for other configurations to inherit
    """
    SITE_NAME = 'FlaskForum'
    SECURITY_PASSWORD_SALT = load_security_file('security.key')
    SECRET_KEY = load_security_file('secret.key')
    WTF_CSRF_ENABLED = True
    BCRYPT_LOG_ROUNDS = 13
    UPLOAD_FOLDER = 'uploads'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DEBUG = True
    SQL_ALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}