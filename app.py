from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Set secret key -- turn into env var
app.config['SECRET_KEY'] = 'cfdfb214f97bb74e2f6d51bc2ec404ea'

@app.route('/')
def home():  # put application's code here
    return render_template('home.html', title='Home')

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
        flash('Welcome back!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run()
