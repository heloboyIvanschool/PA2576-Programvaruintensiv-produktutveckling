from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html') # homepage kan ändra vilekn sida vi sk agå till när html sidan är klar