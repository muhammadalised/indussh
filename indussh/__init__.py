from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from indussh.config import DevelopmentConfig, ProductionConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db = SQLAlchemy(app)
    bcrypt =  Bcrypt(app)

    return app