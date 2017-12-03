from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from ..models import Post, SubForum, Comment, Message, User
from ..auth.forms import CommentForm, SearchForm
from .. import db
from utils import Utils

from . import home

# TEMP ROUTING


@home.route('/nav')
def navigation():
    return render_template('nav.html')

# END TEMP ROUTING


@home.route('/')
def homepage():
    sub_forums = SubForum.query.order_by('is_pinned desc')
    return render_template(
                            'home/index.html',
                            title='Flask Forum',
                            forums=sub_forums,
                            search_form=SearchForm()
                        )


@home.route('/acc')
@login_required
def dash():
    messages = Message.query.filter_by(recipient=current_user.id)
    msg_count = 0
    for message in messages:
        if not message.is_read:
            msg_count += 1
    return render_template(
                            'home/dash.html',
                            title='Flask Forum',
                            message_count=msg_count,
                            search_form=SearchForm()
                        )


@home.route('/post/<route>', methods=['GET', 'POST'])
def view_post(route):
    comments = []
    post = Post.query.filter_by(route=route).first()
    sub = SubForum.query.filter_by(id=post.sub_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
                        post_id=post.id,
                        author=current_user.id,
                        content=form.comment.data,
                        date=Utils.get_datetime()
                    )
        db.session.add(comment)
        db.session.commit()

    if post is not None:
        comments_db = Comment.query.filter_by(post_id=int(post.id))
        for comment in comments_db:
            user = User.query.filter_by(id=comment.author).first()
            comm = {
                'content': comment.content,
                'author': user.username,
                'date': comment.date,
                'id': comment.id
            }
            comments.append(comm)
    return render_template(
                            'home/post.html',
                            post=post,
                            comments=comments,
                            form=form,
                            sub=sub,
                            search_form=SearchForm(),
                            include_control=True
                        )


@home.route('/sb/<route>')
def view_sub(route):
    sub = SubForum.query.filter_by(route=route).first()
    posts_arr = Post.query.filter_by(sub_id=sub.id).order_by('is_pinned desc')
    posts = []
    if posts_arr:
        for p in posts_arr:
            if not p.is_deleted:
                p.count = Comment.query.filter_by(post_id=p.id).count()
                posts.append(p)
    return render_template(
                            'home/sub.html',
                            sub=sub,
                            posts=posts,
                            search_form=SearchForm(),
                            include_control=True
                        )


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
        messages_db = Message.query.filter_by(
                                            recipient=current_user.id
                                        ).order_by('is_read desc')
        count = 0
        messages = []
        for message in messages_db:
            sender = User.query.filter_by(id=message.sender).first()
            mess = {
                'id': message.id,
                'subject': message.subject,
                'sender': sender.username,
                'is_read': message.is_read
            }
            messages.append(mess)
        return render_template('home/messages.html', messages=messages)
    else:
        return redirect(url_for('home.homepage'))


@home.route('/msg/<id>')
def view_message(id):
    if current_user.is_authenticated:
        message = Message.query.get(id)
        sender = User.query.filter_by(id=message.sender).first()
        message.is_read = True
        message.sender_username = sender.username
        db.session.commit()
        return render_template('home/message.html', message=message)
    else:
        return redirect(url_for('home.homepage'))


@home.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print('Search term passed | {}'.format(form.search.data))
        posts = Post.query.filter(
            Post.name.like("%" + form.search.data + "%")
        ).all()
        subs = []
        for post in posts:
            sub = SubForum.query.filter_by(id=post.sub_id)
            subs.append(sub)
        return render_template(
                                'home/results.html',
                                posts=posts,
                                term=form.search.data,
                                search_form=form,
                                subs=subs
                            )
    else:
        print(form.errors)
    return render_template('home/results.html')
