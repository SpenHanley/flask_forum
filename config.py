class Config(object):
    """
    Common configuration options
    """
    pass


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
