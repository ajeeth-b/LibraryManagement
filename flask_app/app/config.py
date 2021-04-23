class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'ThereIsNoSecretInTheWorld'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
