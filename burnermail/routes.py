import string

import flask_login
import random
from burnermail import app, db, bcrypt
from burnermail.forms import RegistrationForm, LoginForm, BurnerForm
from burnermail.models import User, BurnerEmail
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

LETTERS = string.ascii_letters

@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    if current_user.is_authenticated:
        form = BurnerForm()
        if form.validate_on_submit():
            forwards_to = form.forwards_to.data

            # Generates burner email address
            def generate_burner():
                amount = random.randrange(6, 11)
                ret = ''.join(random.choice(LETTERS) for _ in range(amount)).join('@stagec.xyz')
                return BurnerEmail(burner_email=ret, forwards_to=forwards_to, user_id=current_user.get_id())

            burner = generate_burner()
            while BurnerEmail.query.filter_by(burner_email=burner.burner_email).first():
                # Continue to generate burners if we generate one that is already in the DB (highly unlikely).
                burner = generate_burner()

            db.session.add(burner)
            db.session.commit()
            return render_template('home.html', title='Home', form=form)

    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash(f'Login successful. Welcome back!', 'success')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Account route
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='User Account')
