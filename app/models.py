from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User: {}'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SubForum(db.Model):
    __tablename__ = 'subs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    route = db.Column(db.String(8), unique=True)
    modified = db.Column(db.DateTime)
    is_pinned = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'Sub Name: {}'.format(self.name)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(192))
    content = db.Column(db.String(1024))
    route = db.Column(db.String(8), unique=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subs.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    anonymous = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime)
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)
    is_deleted = db.Column(db.Boolean, default=False)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(256))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    date = db.Column(db.DateTime)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent = db.Column(db.DateTime)


class ErrorLogs(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    error = db.Column(db.String(16))
    details = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
