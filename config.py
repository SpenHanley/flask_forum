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


class ProductionConfig(Config):
    """
    Production config
    """
    DEBUG = False
    SQLALCHEMY_DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
