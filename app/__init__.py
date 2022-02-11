from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


bootstrap = Bootstrap()
mail = Mail()
bcrypt = Bcrypt()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.users.roues.routes import users
    app.register_blueprint(users)

    from app.posts.roues.routes import posts
    app.register_blueprint(posts)

    from app.admin.routes.routes import admin
    app.register_blueprint(admin)

    from app.errors.errors.routes import errors
    app.register_blueprint(errors)

    from app.models.models.models import User, Post

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Post=Post)
    return app
