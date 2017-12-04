from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from ..models import Comment, Message, User
from ..auth.forms import CommentForm
from .. import db
from utils import Utils

from . import user


@user.route('/')
@login_required
def homepage():
    messages = Message.query.filter_by(recipient=current_user.id)
    new_msg_count = 0
    msg_count = 0
    for message in messages:
        if not message.is_read:
            # This is the total number of unread messages
            new_msg_count += 1
        # This is the total number of messages
        msg_count += 1

    return render_template(
        'user/index.html',
        title='Account',
        message_count=msg_count,
        new_message_count=new_msg_count
    )


@user.route('/inbox')
@login_required
def inbox_page():
    messages = Message.query.filter_by(
        recipient=current_user.id
    ).order_by("is_read desc")
    count = 0
    inbox = []
    for message in messages:
        sender = User.query.filter_by(id=message.sender).first()
        message_body = {
            'message_id': message.id,
            'message_subject': message.subject,
            'message_sender_name': sender.username,
            'message_is_read': message.is_read
        }
        inbox.append(message_body)
    return render_template('user/messages.html', messages=inbox)


@user.route('/message/<id>')
@login_required
def message_page(id):
    message = Message.query.get(id)
    sender = User.query.filter_by(id=message.sender).first()
    message.is_read = True
    message.sender_username = sender.username
    db.session.commit()
    # TODO: Check if the sender id is already a member variable of message
    return render_template('user/message.html', message=message)


@user.route('/profile/<id>')
def profile_page(id):
    userProfile = User.query.get(id)
    print(userProfile)
    if userProfile is None:
        return redirect(url_for('user.homepage'))
    return render_template('user/profile.html', user=userProfile)
