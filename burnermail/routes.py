import string
import random

from datetime import datetime, timedelta

import burnermail
from burnermail import app, db, bcrypt
from burnermail.forms import RegistrationForm, LoginForm, BurnerForm, AccountUpdateForm, AccountForwardForm
from burnermail.models import User, BurnerEmail, ForwardAddress
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc

NUMBERS = [x for x in range(1, 10)]
WORDS = list(burnermail.all_words)


@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    burner_form = BurnerForm()

    if current_user.is_authenticated:
        burner_form.forwards_to.choices = [x.email for x in current_user.forward_addresses]

        if burner_form.validate_on_submit():
            forwards_to = burner_form.forwards_to.data
            description = burner_form.description.data

            # Generates burner email address with two words and two numbers
            def generate_burner():
                words = [random.choice(WORDS) for _ in range(2)]
                numbers = [str(random.choice(NUMBERS)) for _ in range(2)]
                ret = ''.join(words) + ''.join(numbers) + '@stagec.xyz'
                return BurnerEmail(burner_email=ret, forwards_to=forwards_to, description=description,
                                   user_id=current_user.get_id())

            burner = generate_burner()
            while BurnerEmail.query.filter_by(burner_email=burner.burner_email).first():
                # Continue to generate burners if we generate one that is already in the DB (highly unlikely).
                burner = generate_burner()

            db.session.add(burner)
            db.session.commit()
            return redirect(url_for('home'))
        elif request.method == 'GET':
            recent_burner = BurnerEmail.query.filter_by(user_id=current_user.get_id()).order_by(
                desc(BurnerEmail.date_created)).first()

            if recent_burner and recent_burner.date_created > datetime.utcnow() - timedelta(seconds=1):
                burner_form.forwards_to.data = recent_burner.forwards_to
                burner_form.description.data = recent_burner.description
                burner_form.burner_email.data = recent_burner.burner_email

    return render_template('home.html', title='Home', form=burner_form)


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
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_form = AccountUpdateForm()
    add_forward_form = AccountForwardForm()
    if update_form.submit_update.data and update_form.validate_on_submit():
        current_user.email = update_form.email.data
        db.session.commit()
        flash(f'Your account has been updated. New Email: {update_form.email.data}', 'success')
        return redirect(url_for('account'))
    if add_forward_form.submit_forward.data and add_forward_form.validate_on_submit():
        new_forward = ForwardAddress(email=add_forward_form.email.data, user_id=current_user.get_id())
        db.session.add(new_forward)
        db.session.commit()
        flash(
            f'Successfully added forward address: {add_forward_form.email.data}. Please check your inbox for verification.',
            'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        update_form.email.data = current_user.email
    return render_template('account.html', title='User Account', update_form=update_form,
                           add_forward_form=add_forward_form)


# Deletes burner emails from the database
@app.route('/delete/burner/<int:id>', methods=['POST'])
@login_required
def delete_burner(id):
    BurnerEmail.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Burner deleted successfully.', 'info')
    return redirect(url_for('account'))


# Deletes forward addresses from the database
@app.route('/delete/forward_address/<int:id>', methods=['POST'])
@login_required
def delete_forward_address(id):
    # Find all burner emails associated with this forward address and delete them.
    match_query = ForwardAddress.query.filter_by(id=id)
    match = match_query.first()
    BurnerEmail.query.filter_by(forwards_to=match.email).delete()
    match_query.delete()
    db.session.commit()
    flash(f'Forward address deleted successfully. All associated burners have been removed.', 'info')
    return redirect(url_for('account'))


@app.route('/webhook', methods=['POST'])
def webhook():
    return request.args
