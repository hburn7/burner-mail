from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
# Set secret key -- turn into env var
app.config['SECRET_KEY'] = 'cfdfb214f97bb74e2f6d51bc2ec404ea'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    burner_emails = db.relationship('BurnerEmail', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.date_created}')"

class BurnerEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    burner_email = db.Column(db.String(128), unique=True, nullable=False)
    forwards_to = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BurnerEmail('{self.id}', '{self.burner_email}', {self.forwards_to}, {self.date_created}'"

@app.route('/')
def home():  # put application's code here
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.email.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@test.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run()
