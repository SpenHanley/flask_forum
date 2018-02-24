import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from utils import Utils as utils


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(64),
        index=True,
        unique=True
    )

    username = db.Column(
        db.String(64),
        index=True,
        unique=True
    )

    password_hash = db.Column(
        db.String(128)
    )

    registered_on = db.Column(
        db.DateTime,
        nullable=False
    )

    profile_route = db.Column(
        db.String(6), unique=True
    )

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    confirmed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    confirmed_on = db.Column(
        db.DateTime,
        nullable=True
    )

    use_icons = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    timeformat = db.Column(
        db.String(16),
        default=True
    )

    def __init__(self, email, username, password, confirmed, admin=False, confirmed_on=None):
        self.email = email
        self.username = username
        self.password = password
        self.registered_on = datetime.datetime.utcnow()
        # This is generated here as it makes no sense to generate it in the route file
        self.profile_route = utils.generate_url(6)
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

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

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(64),
        unique=True
    )

    description = db.Column(db.String(128))
    route = db.Column(db.String(8), unique=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    pinned = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __init__(self, title, description, pinned=False):
        self.title = title
        self.description = description
        self.route = utils.generate_url(8)
        self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        self.pinned = pinned

    @staticmethod
    def get_all():
        return SubForum.query.all()

    def __repr__(self):
        return 'Sub Name: {}'.format(self.title)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    content = db.Column(db.String(1024))
    route = db.Column(db.String(8), unique=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subs.id'))

    author_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    anonymous = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)

    pinned = db.Column(db.Boolean,
                       default=False,
                       nullable=False)

    is_deleted = db.Column(db.Boolean)

    @staticmethod
    def get_all():
        return Post.query.all()

    def __repr__(self):
        return 'Post Name: {}'.format(self.title)

    def __init__(self, title, content, sub_id, author_id, anonymous=False, pinned=False, is_deleted=False):
        self.title = title
        self.content = content
        self.sub_id = sub_id
        self.author_id = author_id
        self.anonymous = anonymous
        self.created_on = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        self.route = utils.generate_url(8)
        self.pinned = pinned
        self.is_deleted = is_deleted


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(256))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    date = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)  # Displays when the comment was updated
    edited = db.Column(db.Boolean,
                       default=False,
                       nullable=False)

    def __init__(self, author, content, post_id, edited=False):
        self.author = author
        self.content = content
        self.post_id = post_id
        self.edited = edited


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    sent = db.Column(db.DateTime)

    def __init__(self, recipient, sender, subject, message, is_read=False):
        self.recipient = recipient
        self.sender = sender
        self.subject = subject
        self.message = message
        self.is_read = is_read
        self.sent = datetime.datetime.utcnow()


class ErrorLogs(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    error = db.Column(db.String(16))
    details = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)


class Complaint(db.Model):
    __tablename__ = 'complaint'

    id = db.Column(db.Integer, primary_key=True)
    plaintiff_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    suspect_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, nullable=True)
    message_id = db.Column(db.Integer, nullable=True)
    complaint_body = db.Column(db.String(512), nullable=False)
    assigned = db.Column(db.Boolean, default=False, nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, plaintiff, suspect, complaint_body, comment_id=None, message_id=None):
        self.plaintiff_id = plaintiff
        self.suspect_id = suspect
        self.complaint_body = complaint_body
        self.comment_id = comment_id
        self.message_id = message_id
