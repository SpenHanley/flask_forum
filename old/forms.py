from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(FlaskForm):
    post_name = StringField('Name', validators=[DataRequired()])
    post_text = StringField('Post Text', validators=[DataRequired()])
    post_sub = SelectField('Parent Sub', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    confirmation = StringField('Confirm Email', validators=[DataRequired()])


class SubForm(FlaskForm):
    sub_name = StringField('Name', validators=[DataRequired()])
    sub_desc = StringField('Post Text', validators=[DataRequired()])