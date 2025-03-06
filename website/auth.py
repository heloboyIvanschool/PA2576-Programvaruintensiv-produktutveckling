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
        favorite_genre = request.form.get('favorite_genre')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if password != password_confirm:
            flash('Passwords do not match.', category='error')
            return redirect(url_for('auth.sign_up'))

        # failchecks här
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')

        else:
            new_user = User(username=username, email=email, favorite_genre=favorite_genre, password=generate_password_hash(password)) #profile_picture=profile_pic,
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

        # user_exists = User.query.filter_by(username=username).first()
        # email_exists = User.query.filter_by(email=email).first()

        # if user_exists:
        #     flash('Username already exists.', category='error') # sucsess
        #     return redirect(url_for('register'))

    return render_template('sign_up.html', user=current_user) #register