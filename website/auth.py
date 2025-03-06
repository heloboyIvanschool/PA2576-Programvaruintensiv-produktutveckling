from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.hmtl')

@auth.route('/logout')
def logout():
    return render_template('logout.hmtl')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') #confirm password?
        favorite_genre = request.form.get('favorite_genre')

        # failchecks här

        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Username already exists.', category='error') # sucsess
            return redirect(url_for('register'))

    return render_template('sign_up.hmtl') #register