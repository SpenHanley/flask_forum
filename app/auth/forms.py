from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User, Post, SubForum


class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    admin = BooleanField('Admin')
    confirmed = BooleanField('Set Confirmed')
    submit = SubmitField('Edit')


class CreateUserForm(FlaskForm):
    # None of this should have any effect on the form attempting to submit before data has been entered
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Admin')
    confirmed = BooleanField('Set Confirmed')
    submit = SubmitField('Create')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    post_content = TextAreaField('Post Content', validators=[DataRequired()])
    anonymous = BooleanField('Post Anonymously', default=False)
    submit = SubmitField('Create Post')

    def validate_title(self, field):
        if Post.query.filter_by(title=field.data).first():
            raise ValidationError('Post name already in use')


class DestroyPostForm(FlaskForm):
    reason = TextAreaField('Reason for deletion')
    submit = SubmitField('Delete Comment')


class DeleteCommentForm(FlaskForm):
    reason = TextAreaField('Reason for deletion')
    submit = SubmitField('Delete Post')


class MessageForm(FlaskForm):
    recipient = StringField('Recipient Username', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    send = SubmitField('Send Message')


class EditCommentForm(FlaskForm):
    content = StringField('Comment')
    submit = SubmitField('Update Comment')

class SearchForm(FlaskForm):
    search = StringField('Search')


class RegistrationForm(FlaskForm):

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    # TODO: Attempt to check email as it is being entered to ensure that it is available
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    
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
    comment = TextAreaField('Comment')
    submit = SubmitField('Post Comment')


class SubForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    pinned = BooleanField('Pin Sub Forum')
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

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')
