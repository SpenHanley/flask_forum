from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from ..models import Post, SubForum, Comment, Message, User
from ..auth.forms import CommentForm
from .. import db
from utils import Utils

from . import home


@home.route('/')
def homepage():
    sub_forums = SubForum.query.order_by('is_pinned desc')
    return render_template('home/index.html', title='Flask Forum', forums=sub_forums)


@home.route('/acc')
@login_required
def dash():
    messages = Message.query.filter_by(recipient=current_user.id)
    msg_count = 0
    for message in messages:
        if not message.is_read:
            msg_count += 1
    return render_template('home/dash.html', title='Flask Forum', message_count=msg_count)


@home.route('/post/<route>', methods=['GET', 'POST'])
@login_required
def view_post(route):
    global comments
    post = Post.query.filter_by(route=route).first()
    sub = SubForum.query.filter_by(id=post.sub_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(post_id=post.id, author=current_user.id, content=form.comment.data,
                          date=Utils.get_datetime())
        db.session.add(comment)
        db.session.commit()

    if post is not None:
        comments = Comment.query.filter_by(post_id=int(post.id))
    return render_template('home/post.html', post=post, comments=comments, form=form, sub=sub)


@home.route('/sb/<route>')
def view_sub(route):
    sub = SubForum.query.filter_by(route=route).first()
    posts_arr = Post.query.filter_by(sub_id=sub.id).order_by('is_pinned desc')
    posts = []
    if posts_arr:
        for p in posts_arr:
            if not p.is_deleted:
                posts.append(p)
                p.count = Comment.query.filter_by(post_id=p.id).count()
    return render_template('home/sub.html', sub=sub, posts=posts)


@home.route('/pns/<route>', methods=['GET', 'POST'])
def pin_sub(route):
    sub = SubForum.query.filter_by(route=route).first()
    pinned = sub.is_pinned
    if pinned:
        pinned = False
    else:
        pinned = True
    sub.is_pinned = pinned
    db.session.commit()
    return redirect(url_for('home.homepage'))


@home.route('/pnp/<route>', methods=['GET', 'POST'])
def pin_post(route):
    post = Post.query.filter_by(route=route).first()
    pinned = post.is_pinned
    if pinned:
        pinned = False
    else:
        pinned = True
    post.is_pinned = pinned
    db.session.commit()
    return redirect(url_for('home.homepage'))


@home.route('/inb')
def view_inbox():
    if current_user.is_authenticated:
        messages = Message.query.filter_by(recipient=current_user.id).order_by('is_read desc')
        count = 0
        for message in messages:
            sender = User.query.filter_by(id=message.sender).first()
            message.sender_username = sender.username
        return render_template('home/messages.html', messages=messages)
    else:
        return redirect(url_for('home.homepage'))


@home.route('/msg/<id>')
def view_message(id):
    if current_user.is_authenticated:
        message = Message.query.get(id)
        message.is_read = True
        db.session.commit()
        return render_template('home/message.html', message=message)
    else:
        return redirect(url_for('home.homepage'))
