import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") # mysql://username:password@server/db

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = '5d15034ccb53145cc8fb6b1bddc0c400'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = "secret_for_test_environment"
    OAUTHLIB_INSECURE_TRANSPORT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False