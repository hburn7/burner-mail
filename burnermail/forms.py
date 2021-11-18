from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from burnermail.models import User, BurnerEmail

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
    burner_email = StringField('Burner Email')
    submit = SubmitField('Generate')

    def validate_email(self, email):
        user = BurnerEmail.query.filter_by(forwards_to=email.data).first()
        if user:
            raise ValidationError('Another account is already forwarding emails to this address.')

class AccountForwardForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit_forward = SubmitField('Add')

    def validate_email(self, email):
        burner = BurnerEmail.query.filter_by(forwards_to=email.data).first()
        if burner:
            raise ValidationError('Another account is already forwarding emails to this address.')


class AccountUpdateForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit_update = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account with this email already exists.')

class ForwardSelectForm(FlaskForm):
    email = SelectField('Forward Address', validators=[DataRequired(), Email()])



