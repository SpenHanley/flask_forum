from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import *
from .. import db
from ..models import User
from utils import Utils


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered')

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/lg', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect(url_for('home.dash'))
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form)


@auth.route('/lo')
@login_required
def logout():
    logout_user()
    flash('You have sucessfully logged out')
    return redirect(url_for('auth.login'))


@auth.route('/cs', methods=['GET', 'POST'])
@login_required
def create_sub():
    if current_user.is_admin:
        form = SubForm()
        if form.validate_on_submit():
            url = Utils.generate_url(8)
            forum = SubForum(name=form.title.data, description=form.description.data, url=url)
            db.session.add(forum)
            db.session.commit()
            print('It worked')
            flash('Sub Forum Created')
            return redirect(url_for('home.view_post', url=url))
        return render_template('auth/sub.html', form=form)
    else:
        return redirect(url_for('home.homepage'))
