from flask import Blueprint, request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from . import login_manager

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({"error": "Login required"}), 401

    data = request.json
    print("Login attempt with data:", data)  # Add this line to see the login data
    email = data.get('email')
    password = data.get('password')

    print(f"Attempting login with email: {email}")  # Add this logging

    user = User.query.filter_by(email=email).first()

    if not user:
        print(f"No user found with email: {email}")  # Log if user not found
        return jsonify({"error": "Email not found"}), 401

    print(f"User found: {user.username}, verifying password")  # Log user found

    if not user.check_password(password):
        print("Password verification failed")  # Log password failure
        return jsonify({"error": "Incorrect password"}), 401

    print("Password verified, logging in user")  # Log successful verification
    login_user(user, remember=True)

    next_url = request.args.get('next')
    print(f"Login successful for {user.username}, redirecting to: {next_url or '/profile'}")

    if next_url:
        return jsonify({"message": "Logged in successfully", "next": next_url}), 200
    else:
        return jsonify({"message": "Logged in successfully", "next": "/profile"}), 200

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

    if not username or not email or not password or not password_confirm:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already exists"}), 409

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already exists"}), 409

    if password != password_confirm:
        return jsonify({"error": "Passwords do not match"}), 400

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


@auth.route('/test', methods=['GET'])
def test():
    return "Server is running!", 200

# onödig atm
@auth.route('/auth-status', methods=['GET'])
def auth_status():
    """ Kollar om en användare är inloggad och returnerar deras data. """
    if current_user.is_authenticated:
        return jsonify({"logged_in": True, "username": current_user.username}), 200
    else:
        return jsonify({"logged_in": False}), 200

