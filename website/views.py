from flask import Blueprint, jsonify, send_from_directory
from flask_login import login_required, current_user

# Skapar en Blueprint för views (frontend och hemsida)
views = Blueprint('views', __name__)

@views.route('/')
def serve_react():
    """
    Serverar React-appens index.html från build-mappen.

    Returns:
        Response: HTML-sidan från React-byggmappen.
    """
    return send_from_directory('../react-frontend/build', 'index.html')


@views.route('/')
# @login_required  # Avkommentera vid behov av autentisering
def home():
    """
    Returnerar ett välkomstmeddelande i JSON-format.

    Returns:
        Response: JSON med välkomsttext och användarnamn.
    """
    return jsonify({
        "message": "Welcome to Resonate!",
        "user": "testuser"  # Byt ut till current_user.username när login är aktiverat
    })
