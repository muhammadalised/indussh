import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SESSION_TYPE=os.environ.get('SESSION_TYPE')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PRODUCTS_DATA_PATH = os.path.join(basedir, 'seed_data/Products.csv')
    PROFILE_IMAGES_PATH = 'static/uploads/profile_images'
    PRODUCT_IMAGES_PATH = 'static/uploads/product_images'

    PROFILE_IMAGE_SIZE = (125, 125)
    PRODUCT_IMAGE_SIZE = (480, 340)

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    OAUTHLIB_INSECURE_TRANSPORT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
config = {
    'development':  DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}