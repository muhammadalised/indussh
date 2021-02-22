from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from indussh.config import DevelopmentConfig
from flask_session import Session

db = SQLAlchemy()
bcrypt =  Bcrypt()
sess = Session()
# login_manager = LoginManager()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    db.init_app(app)
    bcrypt.init_app(app)
    sess.init_app(app)
    # login_manager.init_app(app)

    from indussh.main.routes import main
    from indussh.products.routes import products

    app.register_blueprint(main)
    app.register_blueprint(products)

    return app