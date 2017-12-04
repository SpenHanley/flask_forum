from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import *
from .. import db
from ..models import User, Message, Comment
from utils import Utils


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registered')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect(url_for('user.homepage'))
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have sucessfully logged out')
    return redirect(url_for('auth.login'))


@auth.route('/create_sub', methods=['GET', 'POST'])
@login_required
def create_sub():
    if current_user.is_authenticated:
        form = SubForm()
        if form.validate_on_submit():
            sUrl = Utils.generate_url(length=8)
            forum = SubForum(
                name=form.title.data,
                description=form.description.data,
                route=sUrl,
                modified=Utils.get_datetime()
            )
            db.session.add(forum)
            db.session.commit()
            print('It worked')
            flash('Sub Forum Created')
            return redirect(url_for('home.view_sub', route=sUrl))
        else:
            print(form.errors)
            print(form.title.errors)
            print(form.description.errors)
        return render_template('auth/sub.html', form=form)
    else:
        return redirect(url_for('home.homepage'))


@auth.route('/create_post/<p>', methods=['GET', 'POST'])
@login_required
def create_post(p):
    if current_user.is_authenticated:
        form = PostForm()
        sub = SubForum.query.filter_by(route=p).first()
        if form.validate_on_submit():
            sUrl = Utils.generate_url(8)
            post = Post(
                name=form.title.data,
                description=form.description.data,
                content=form.post_content.data,
                anonymous=form.anonymous.data,
                route=sUrl,
                sub_id=sub.id,
                created_on=Utils.get_datetime(),
                author_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            flash('Post Created')
            return redirect(url_for('home.view_post', route=sUrl))
        return render_template('auth/post.html', form=form, p=p)
    else:
        return redirect(url_for('home.homepage'))


@auth.route('/delete_post/<route>', methods=['GET', 'POST'])
@login_required
def del_post(route):
    if current_user.is_authenticated and current_user.is_admin:
        form = DestroyPostForm()
        if form.validate_on_submit():
            post = Post.query.filter_by(route=route).first()
            post.is_deleted = True

            message = Message(
                recipient=post.author_id,
                sender=current_user.id,
                subject='Post Deletion',
                message='Your post: ' +
                post.name + ' was deleted for: ' +
                form.reason.data + '.'
            )

            db.session.add(message)
            db.session.commit()
            sub = SubForum.query.filter_by(id=post.sub_id).first()
            return redirect(url_for('home.view_sub', route=sub.route))
        return render_template('auth/del_post.html', form=form, route=route)
    else:
        return redirect(url_for('home.homepage'))


@auth.route('/send', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        rec = User.query.filter_by(username=form.recipient.data).first()

        message = Message(
            recipient=rec.id,
            sender=current_user.id,
            message=form.message.data,
            sent=Utils.get_datetime(),
            subject=form.subject.data
        )

        db.session.add(message)
        db.session.commit()
        flash('Message sent')
        return redirect(url_for('home.dash'))
    return render_template('auth/send_message.html', form=form)


@auth.route('/send/<id>', methods=['GET', 'POST'])
@login_required
def send_message_with_rec(id):
    form = MessageForm()
    recipient = User.query.filter_by(id=id).first()
    form.recipient.data = recipient.username
    if form.validate_on_submit():

        message = Message(
            recipient=recipient.id,
            sender=current_user.id,
            message=form.message.data,
            sent=Utils.get_datetime(),
            subject=form.subject.data
        )

        db.session.add(message)
        db.session.commit()
        flash('Message sent')
        return redirect(url_for('home.dash'))
    else:
        print(form.errors)

    return render_template('auth/send_message.html', form=form)


@auth.route('/delete_message/<id>')
def delete_message(id):
    Message.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('home.view_inbox'))


@auth.route('/reply_message/<id>')
def reply_message(id):
    return redirect(url_for('auth.send_message_with_rec', id=id))


@auth.route('/delete_comment/<id>', methods=['GET', 'POST'])
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    post = Post.query.filter_by(id=comment.post_id).first()
    form = DeleteCommentForm()

    if form.validate_on_submit():

        message = Message(
            recipient=comment.author,
            sender=current_user.id,
            subject='Post Deletion',
            message='Your comment on: ' +
            post.name + ' was deleted for: ' +
            form.reason.data + '.'
        )

        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('home.view_post', route=post.route))

    if current_user.id is not comment.author:
        return render_template('auth/del_comment.html', form=form, id=id)
    else:
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('home.view_post', route=post.route))
