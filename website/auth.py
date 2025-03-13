from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Looged in')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incoret password')
        else:
            flash('email does not exist')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Kontrollera att fälten inte är tomma
        if not username or not email or not password or not password_confirm:
            flash("All fields are required.", category="error")
            return redirect(url_for("auth.sign_up"))

        # Kontrollera om lösenord matchar
        if password != password_confirm:
            flash('Passwords do not match.', category='error')
            return redirect(url_for('auth.sign_up'))

        # Kontrollera om användarnamn eller e-post redan finns
        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=username).first()

        if user_by_email:
            flash('Email already exists.', category='error')
        elif user_by_username:
            flash('Username already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        else:
            # Skapa ny användare om inga fel hittas
            new_user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
