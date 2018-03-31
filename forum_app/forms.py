from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=DataRequired())
    password = PasswordField('Password', validators=DataRequired())
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=DataRequired())
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=DataRequired())
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ])
    register = SubmitField('Register')

    def check_username_available(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use')
