from flask import render_template, url_for, redirect, session
from flask_login import login_required, current_user
from ..models import Message, User, Post
from app.forms import ProfileForm, SearchForm
from .. import db
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from . import user


@user.route('/<route>')
@login_required
def homepage(route):
    session['room'] = 'global_chat'
    messages = Message.query.filter_by(recipient=current_user.id)
    user = User.query.filter_by(profile_route=route).first()
    if current_user != user:
        return redirect(url_for('home.homepage'))
    new_msg_count = 0
    msg_count = 0
    for message in messages:
        if not message.is_read:
            # This is the total number of unread messages
            new_msg_count += 1
        # This is the total number of messages
        msg_count += 1

    # Does the profile_image contain an external link
    external = ('http://' in user.profile_image) or ('https://' in user.profile_image)

    return render_template(
        'user/index.html',
        title='Account',
        message_count=msg_count,
        new_message_count=new_msg_count,
        external=external,
        user=user,
        profile_url=current_user.profile_route,
        form=ProfileForm()
    )


@user.route('/update/<route>', methods=['POST'])
def update(route):
    user = User.query.filter_by(profile_route=route)
    form = ProfileForm()

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data

        # Let's move the and rename the uploaded file
        f = form.profile_image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
                app.root_path,
                'static',
                'uploads',
                'images',
                filename
            )
        )
        # Now we set the profile image path for the user
        user.profile_image = 'uploads/images/'+filename
        # Let's stick this in the database
        db.session.add(user)
        db.session.commit()
    else:
        print('Something went wrong')


@user.route('/inbox')
@login_required
def inbox_page():
    messages = Message.query.filter_by(
        recipient=current_user.id
    ).order_by(desc('is_read'))
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
    return render_template('user/messages.html', messages=inbox, search_form=SearchForm())


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


@user.route('/<route>/profile')
@login_required
def profile_page(route):
    userProfile = User.query.filter_by(profile_route=route).first()
    posts = Post.query.filter_by(author_id=userProfile.id).filter_by(anonymous=False).all()
    print(userProfile)
    user = {
        'username': userProfile.username,
        'uid': userProfile.id,
        'profile_image': userProfile.profile_image
    }
    if userProfile is None:
        return redirect(url_for('registered_user.homepage'))

    external = ('http://' in userProfile.profile_image) or ('https://' in userProfile.profile_image)

    return render_template('user/profile.html', user=user, external=external, posts=posts)


@user.route('/<route>/edit_profile')
@login_required
def edit_profile(route):
    user = User.query.filter_by(profile_route=route)
    template = '''
    <h1>Not Implemented</h1>
    <p>
    This feature has yet to be implemented
    </p>
    '''
    return template


@user.route('/chat')
@login_required
def chat():
    name = current_user.username
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('home.homepage'))

    return render_template('user/chat.html', name=name, room=room)
