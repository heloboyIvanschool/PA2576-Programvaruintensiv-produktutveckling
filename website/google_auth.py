from flask import Blueprint, redirect, url_for, session, flash
from flask_login import login_user, current_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized

from . import db
from .models import User, OAuth
import os

#Här skapas en blueprint för att kunna route:a för att använda OAuth
#Skickar vidare dom till Google login och säger att jag vill ha deras profilbild + email

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENTID"),
    client_secret=os.getenv("GOOGLE_CLIENTSECRET"),
    scope=["profile", "email"],
    redirect_url="/login/google/authorized",
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)

#oauth_routes är variabeln för att kalla på dett
oauth_routes = Blueprint("oauth", __name__)

#Här kollar jag om användaren redan är inloggad
# Om den är inloggad går den till home annars till Google login 
@oauth_routes.route("/login/google")
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
        
    return redirect(url_for("google.login"))

# Detta är en sk call-back, dvs när vi återgår från Google
# Parametern token är vad google ger oss, om den inte finns har inloggningen misslyckats


@oauth_authorized.connect_via(google_bp)
def google_logged_in(token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

#Här används en Google API som heter OAuth 2 för att kolla den inloggades info
    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", category="error")
        return False
    
#Om det finns info laddas det ner i en json-fil och vi plockar ut email från den infon
    user_info = resp.json()
    email = user_info["email"]
    
    #kollar om emailen är en användare
    user = User.query.filter_by(email=email).first()
    if not user:
        
        #om inte skapar vi en, här får vi lägga till saker
        username = user_info.get("name", email.split("@")[0])
        user = User(
            username=username,
            email=email,
            password="google-oauth"  # vet inte hur vi gör här, vi borde sätta ett random lösen??
        )
        db.session.add(user)
        db.session.commit()
        
    # Log in the user
    login_user(user)
    flash(f"Successfully signed in with Google as {user.username}.", category="success")
    
    # Returnerar false annars skapas en ny token
    return False