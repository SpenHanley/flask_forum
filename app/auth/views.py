import datetime

from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import datetime

from utils import Utils
from . import auth
from app import db
from ..email import send_mail
from ..forms import *
from ..models import User, Message, Comment


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            confirmed=False
        )

        db.session.add(user)
        db.session.commit()

        # token = generate_confirmation_token(user.email)
        # confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        # html = render_template('emails/confirm.html', confirm_url=confirm_url)
        # subject = 'Please confirm your email!'
        # asd = send_mail(user.email, subject, html)

        flash('Confirmation email sent', 'Success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


# @auth.route('/confirm/<token>')
# @login_required
# def confirm_email(token):
#     try:
#         # email = confirm_token(token)
#     except:
#         flash('Confirmation token invalid or has expired.', 'danger')
#     user = User.query.filter_by(email=email).first_or_404()
#     if user.confirmed:
#         flash('Account already confirmed. Please login.', 'success')
#     else:
#         user.confirmed = True
#         user.confirmed_on = datetime.datetime.utcnow()
#         db.session.add(user)
#         db.session.commit()
#         flash('You have confirmed your account. Thanks!', 'success')
#     return redirect(url_for('registered_user.home', route=user.profile_route))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if request.args.get('next'):
                if not 'logout' in request.args.get('next'):
                    return redirect(request.args.get('next'))
                else:
                    return redirect(url_for('user.homepage', route=user.profile_route))

            return redirect(url_for('user.homepage', route=user.profile_route))
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
            forum = SubForum(
                title=form.title.data,
                description=form.description.data
            )
            db.session.add(forum)
            db.session.commit()
            print('It worked')
            flash('Sub Forum Created')
            return redirect(url_for('home.view_sub', route=forum.route))
        else:
            print(form.errors)
            print(form.title.errors)
            print(form.description.errors)
        return render_template('auth/sub.html', form=form)
    else:
        return redirect(url_for('home.homepage'))


@auth.route('/create_post/<sub_route>', methods=['GET', 'POST'])
@login_required
def create_post(sub_route):
    form = PostForm()
    sub = SubForum.query.filter_by(route=sub_route).first()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.post_content.data,
            sub_id=sub.id,
            author_id=current_user.id,
            anonymous=form.anonymous.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Post Created')
        return redirect(url_for('home.view_post', route=post.route))
    else:
        print(form.errors)
    return render_template('auth/post.html', form=form, sub=sub)


@auth.route('/delete_post/<route>', methods=['GET', 'POST'])
@login_required
def delete_post(route):
    form = DeletePostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(route=route).first()
        post.is_deleted = True

        message = Message(
            recipient=post.author_id,
            sender=current_user.id,
            subject='Post Deletion',
            message='Your post: ' +
                    post.title + ' was deleted for: ' +
                    form.reason.data + '.'
        )

        db.session.add(message)
        db.session.commit()
        sub = SubForum.query.filter_by(id=post.sub_id).first()
        return redirect(url_for('home.view_sub', route=sub.route))
    return render_template('auth/delete_post.html', form=form, route=route)


@auth.route('/send', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        rec = User.query.filter_by(username=form.recipient.data).first()

        message = Message(
            recipient=rec.id,
            sender=current_user.id,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(message)
        db.session.commit()
        flash('Message sent')
        return redirect(url_for('home.dash'))
    return render_template('auth/send_message.html', form=form)


@auth.route('/send/<user_id>', methods=['GET', 'POST'])
@login_required
def send_message_with_rec(user_id):
    form = MessageForm()
    recipient = User.query.filter_by(id=user_id).first()
    form.recipient.data = recipient.username
    if form.validate_on_submit():

        message = Message(
            recipient=recipient.id,
            sender=current_user.id,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(message)
        db.session.commit()
        flash('Message sent')
        return redirect(url_for('home.dash'))
    else:
        print(form.errors)

    return render_template('auth/send_message.html', form=form)


@auth.route('/delete_message/<message_id>')
def delete_message(message_id):
    Message.query.filter_by(id=message_id).delete()
    db.session.commit()
    return redirect(url_for('home.view_inbox'))


@auth.route('/reply_message/<message_id>')
def reply_message(message_id):
    return redirect(url_for('auth.send_message_with_rec', id=message_id))


@auth.route('/delete_comment/<comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    post = Post.query.filter_by(id=comment.post_id).first()
    form = DeleteCommentForm()

    if form.validate_on_submit():
        message = Message(
            recipient=comment.author,
            sender=current_user.id,
            subject='Post Deletion',
            message='Your comment on: ' +
                    post.title + ' was deleted for: ' +
                    form.reason.data + '.'
        )

        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('home.view_post', route=post.route))

    if current_user.id is not comment.author:
        return render_template('auth/delete_comment.html', form=form, id=id)
    else:
        Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
        return redirect(url_for('home.view_post', route=post.route))


@auth.route('/update_comment/<comment_id>', methods=['GET', 'POST'])
def update_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    print(comment)

    form = EditCommentForm()

    if form.validate_on_submit():
        print('Form validated')
        comment.content = form.content.data
        comment.edited = True
        comment.updated = Utils.get_datetime()

        print(Utils.get_datetime())

        db.session.add(comment)
        db.session.commit()
    else:
        print('Comment not updated, form did not validate!')

    return render_template('auth/update_comment.html', form=form, comment=comment)


@auth.route('/delete_sub/<route>')
def delete_sub(route):
    sub = SubForum.query.filter_by(route=route).first()
    form = DeleteSubForm()

@auth.route('/edit_sub/<route>', methods=['GET', 'POST'])
def edit_sub(route):
    sub = SubForum.query.filter_by(route=route).first()
    form = EditSubForm()

    if form.validate_on_submit():
        sub.title = form.title.data
        sub.description = form.description.data
        sub.modified = datetime.datetime.utcnow()

        db.session.add(sub)
        db.session.commit()
    else:
        print('Sub not updated, form did not validate!')

    return render_template('auth/update_sub.html', form=form, sub=sub)

@auth.route('/edit_post/<route>', methods=['GET', 'POST'])
def edit_post(route):
    post = Post.query.filter_by(route=route).first()

    form = EditPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        post.modified = datetime.datetime.utcnow()

        db.session.add(post)
        db.session.commit()

    return render_template('auth/edit_post.html', form=form, post=post)
