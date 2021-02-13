from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from indussh.config import DevelopmentConfig

db = SQLAlchemy()
bcrypt =  Bcrypt()
# login_manager = LoginManager()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    db.init_app(app)
    bcrypt.init_app(app)
    # login_manager.init_app(app)

    from indussh.shop.routes import shop

    app.register_blueprint(shop)

    return app