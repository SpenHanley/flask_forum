from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, HiddenField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User, Post, SubForum


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    post_content = TextAreaField('Post Content', validators=[DataRequired()])
    url = StringField('Forum URL')
    submit = SubmitField('Create Sub Forum')

    def validate_title(self, field):
        if Post.query.filter_by(name=field.data).first():
            raise ValidationError('Post name already in use')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    author = HiddenField('Author')  # Author of post
    post = HiddenField('Post')  # ID of post that comment belongs to
    comment = TextAreaField('Comment')
    date = DateTimeField('timestamp')
    submit = SubmitField('Post Comment')


class SubForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Sub Forum')

    def validate_title(self, field):
        if SubForum.query.filter_by(name=field.data).first():
            raise ValidationError('Sub name in use')


class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])

    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')
