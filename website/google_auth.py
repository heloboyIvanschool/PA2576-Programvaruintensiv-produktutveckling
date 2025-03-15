from flask import Blueprint, redirect, url_for, session, flash
from flask_login import login_user, current_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized

from . import db
from .models import User, OAuth
import os

# Create a blueprint for Google OAuth
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

# Define the blueprint
oauth_routes = Blueprint("oauth", __name__)

# Register login/authorized routes
@oauth_routes.route("/login/google")
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
        
    return redirect(url_for("google.login"))

# Signal handler for OAuth login completion
@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", category="error")
        return False
        
    user_info = resp.json()
    email = user_info["email"]
    
    # Find or create user
    user = User.query.filter_by(email=email).first()
    if not user:
        # Create a new user
        username = user_info.get("name", email.split("@")[0])
        user = User(
            username=username,
            email=email,
            password="google-oauth"  # You might want to set a random password here
        )
        db.session.add(user)
        db.session.commit()
        
    # Log in the user
    login_user(user)
    flash(f"Successfully signed in with Google as {user.username}.", category="success")
    
    # Return False so Flask-Dance doesn't create another token
    return False