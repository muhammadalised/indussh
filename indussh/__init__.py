from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session, SqlAlchemySessionInterface
from .config import config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
sess = Session()

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize the flask-sqlalchemy instance
    db.init_app(app)
    # Initialize the migration instance
    migrate.init_app(app, db)
    # Initialize flask session instance
    sess.init_app(app)
    # Configuration for flask session type 'sqlalchemy', creating the session tables in database
    SqlAlchemySessionInterface(app, db, "sessions", "sess_")
    
    bcrypt.init_app(app)
    login_manager.init_app(app)


    from indussh.main.routes import main
    from indussh.products.routes import products
    from indussh.users.routes import users
    from indussh.admin.routes import admin


    app.register_blueprint(main)
    app.register_blueprint(products, url_prefix='/shop')
    app.register_blueprint(users)
    app.register_blueprint(admin, url_prefix='/admin')

    return app
