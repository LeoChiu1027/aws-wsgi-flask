class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

class Development(Config):
    DEBUG = True

class Testing(Config):
    TESTING = True