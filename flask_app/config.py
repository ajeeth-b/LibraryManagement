from os import environ

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'ThereIsNoSecretInTheWorld'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    environ['DATASTORE_DATASET'] = 'ajeeth-internship-app'
    environ['DATASTORE_EMULATOR_HOST'] = 'localhost:8081'
    environ['DATASTORE_EMULATOR_HOST_PATH'] = 'localhost:8081/datastore'
    environ['DATASTORE_HOST'] = 'http://localhost:8081'
    environ['DATASTORE_PROJECT_ID'] = 'ajeeth-internship-app'
