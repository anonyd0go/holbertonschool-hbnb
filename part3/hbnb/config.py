import os


class Config:
    """
    Base configuration class. Contains default configuration settings.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configuration class. Inherits from Config and sets DEBUG to 
    True.
    """
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
