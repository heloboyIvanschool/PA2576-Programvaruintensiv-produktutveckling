from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """ Hanterar inloggning av användare. """

    data = request.json  # Tar emot JSON-data från frontend
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user, remember=True)

    return jsonify({
        "message": "Logged in successfully",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
    }), 200

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """ Hanterar utloggning av användare. """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    """ Hanterar registrering av en ny användare. """

    data = request.json  # Tar emot JSON från frontend
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    if not username or not email or not password or not password_confirm:
        return jsonify({"error": "Missing required fields"}), 400

    if password != password_confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password)
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