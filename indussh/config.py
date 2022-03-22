import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory
basepath = Path()
basedir = str(basepath.cwd())
# Load the environment variables
envars = basepath.cwd() / '.env'
load_dotenv(envars)

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") # mysql://username:password@server/db
    SESSION_TYPE=os.environ.get('SESSION_TYPE')
    FLASK_ADMIN_SWATCH = 'cerulean'

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    OAUTHLIB_INSECURE_TRANSPORT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False