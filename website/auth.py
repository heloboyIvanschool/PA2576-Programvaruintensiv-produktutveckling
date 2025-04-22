from flask import Blueprint, request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from . import login_manager

#Vi skapar en ny blueprint med routes som har med autentisering att göra
auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({"error": "Login required"}), 401

    data = request.json
    print("Login attempt with data:", data)  # Vi printar inloggningsförsöket för att kunna felsöka
    email = data.get('email')
    password = data.get('password')

    print(f"Attempting login with email: {email}")  

    user = User.query.filter_by(email=email).first()

    if not user:
        print(f"No user found with email: {email}")  # För att felsöka
        return jsonify({"error": "Email not found"}), 401

    print(f"User found: {user.username}, verifying password")  # Också felsökning

    if not user.check_password(password):
        print("Password verification failed")  
        return jsonify({"error": "Incorrect password"}), 401

    print("Password verified, logging in user")  # För att se lyckad inloggning
    login_user(user, remember=True)

    # Spara användardata i Flask-sessionen
    session["user_id"] = user.user_id
    session["username"] = user.username

    if 'username' in session:
        print(session['username'])

    next_url = request.args.get('next')
    print(f"Login successful for {user.username}, redirecting to: {next_url or '/profile'}")

    if next_url:
        return jsonify({"message": "Logged in successfully", "next": next_url}), 200
    else:
        return jsonify({"message": "Logged in successfully", "next": "/profile"}), 200
# Här hanterar vi när användaren ska logga ut, kräver att man redan är inloggad.
@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth.route('/signup', methods=['POST'])
def register():
    """ Hanterar registrering av en ny användare. """

    data = request.json
    username = data.get('username').strip()
    email = data.get('email').strip().lower()
    password = data.get('password').strip()
    password_confirm = data.get('password_confirm').strip()

    #Validerar att alla nödvändiga fält finns
    if not username or not email or not password or not password_confirm:
        return jsonify({"error": "Missing required fields"}), 400
    #Kontrollerar om emailen redan finns
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already exists"}), 409
    #Kontrollerar om användarnamnet redan finns
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already exists"}), 409
    #Kollar så lösenordet passar
    if password != password_confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    # Här skapar vi en ny användare
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=True)

    return jsonify({
        "message": "Account created successfully",
        "user": {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201

# Här testade vi så att verifiera att servern funkade 
@auth.route('/test', methods=['GET'])
def test():
    return "Server is running!", 200

# Här kollar vi statusen på användaren, skapades när vi testade sessions.
@auth.route('/auth-status', methods=['GET'])
def auth_status():
    if "user_id" in session:
        return jsonify({
            "logged_in": True,
            "user": {
                "user_id": session["user_id"],
                "username": session["username"]
            }
        }), 200
    else:
        return jsonify({"logged_in": False}), 401

