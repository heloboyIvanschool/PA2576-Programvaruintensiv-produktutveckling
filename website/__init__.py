from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
import os
# from . import db_events # at inte bort

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)

    from .views import views
    from .auth import auth

    from .models import User, OAuth
    

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .google_auth import google_bp, oauth_routes
    app.register_blueprint(google_bp, url_prefix='/login')
    app.register_blueprint(oauth_routes, url_prefix='/')

    from . import db_events


    with app.app_context():
        db.drop_all()
        db.create_all()
        # create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        return User.query.get(int(user_id))

    return app
