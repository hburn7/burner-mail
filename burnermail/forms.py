from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from burnermail.models import User

class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), Length(8, 128), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists.')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BurnerForm(FlaskForm):
    forwards_to = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Generate')


