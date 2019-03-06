class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    DB_URI = 'mongodb+srv://user123:user123@cluster0-ph6ze.mongodb.net/test?retryWrites=true'
    PATH_MODEL = './models/current/nlu'
    TOKENS = {
        'hwvTzW7FJTwEA4XTVNxkWRApa0srOQYu':'app1',
        'hq9Nl0W0FhkObivMA8m8WphUjTlacTfG':'app2'
    }


class ProductionConfig(Config):
    """Configurations for production."""
    DB_NAME = 'nlu_results'

class DevelopmentConfig(Config):
    """Configurations for Development, with a separate development database"""
    DEBUG = True
    DB_NAME = 'nlu_dev'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DB_NAME = 'nlu_test'