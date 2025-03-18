from flask import Blueprint, jsonify, send_from_directory
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def serve_react():
    return send_from_directory('../react-frontend/build', 'index.html')

@views.route('/')
# @login_required
def home():
    return jsonify({"message": "Welcome to Resonate!", "user": "testuser"}) #current_user.username