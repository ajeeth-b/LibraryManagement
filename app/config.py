from os import environ


class Config(object):
    DEBUG = False
    TESTING = False
    GOOGLE_APPLICATION_CREDENTIAL = "path\\to\\credentials.json"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_APPLICATION_CREDENTIAL