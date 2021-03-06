import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'dev_key_h8hfne89vm'
    CSRF_ENABLED = True
    CSRF_SESSION_LKEY = 'dev_key_h8asSNJ9s9=+'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    TWITTER_OAUTH_CONSUMER_KEY = 'BgBZmgEOPL1iUuX0CaRkkN7LD'
    TWITTER_OAUTH_CONSUMER_SECRET = 'ELHh0bo346Xd8zL8xKsSwOayXrPRP0RWTE9RdA5M11TBq0JTLB'

class TestingConfig(DevelopmentConfig):
    TESTING = True

class ProductionConfig(Config):
    PRODUCTION = True

mode = os.environ.get('TFAVFEED_ENV', 'development')
object = DevelopmentConfig
if mode == 'development':
    object = DevelopmentConfig
elif mode == 'testing':
    object = TestingConfig
elif mode == 'production':
    object = ProductionConfig
else:
    raise ValueError("Unknown config mode.")