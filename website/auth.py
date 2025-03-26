from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

#test

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Email not found"}), 401

    if not user.check_password(password):
        return jsonify({"error": "Incorrect password"}), 401

    login_user(user, remember=True)

    return jsonify({"message": "Logged in successfully"}), 200

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
        return jsonify({
            "logged_in": True,
            "user": {
                "user_id": current_user.user_id,
                "username": current_user.username,
                "email": current_user.email
            }
        }), 200
    else:
        return jsonify({
            "logged_in": False,
            "user": None
        }), 200