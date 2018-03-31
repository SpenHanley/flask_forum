from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Model
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from utils import generate
import datetime


class User(UserMixin, Model):
    __tablename__ = 'user'

    id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String(128),
        unique=True,
        nullable=False
    )

    username = Column(
        String(64),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(128)
    )

    role_id = Column(
        Integer,
        ForeignKey('role.id')
    )

    role = relationship(
        'Role',
        backref='user',
        uselist=False
    )

    route = Column(
        String(12),
        default=generate(12)
    )

    registered_on = Column(
        DateTime,
        # This is set when the user registers and won't need changed after that
        default=datetime.datetime.now()
    )

    profile_image = Column(
        String(64),
        default='http://placehold.it/300x300'  # A simple placeholder image
    )

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Forum(Model):
    __tablename__ = 'forum'

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String(64),
        unique=True,
        nullable=False
    )

    description = Column(
        String(256),
        nullable=False
    )

    route = Column(
        String(16),
        default=generate(16)
    )

    
