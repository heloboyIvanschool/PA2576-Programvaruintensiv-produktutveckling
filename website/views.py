from flask import Blueprint, jsonify
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return jsonify({"message": "Welcome to Resonate!", "user": current_user.username})