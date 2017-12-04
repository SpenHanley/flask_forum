from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from . import admin
from ..models import User
from ..auth.forms import EditUserForm, CreateUserForm
from .. import db
from utils import Utils


@admin.route('')
@login_required
def homepage():
    return render_template('admin/index.html')


@admin.route('/user')
@login_required
def show_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@admin.route('/edit_user/<id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    form = EditUserForm()
    user = User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        user = User.query.filter_by(id=id).first()
        user.email = form.email.data
        user.username = form.username.data
        user.is_admin = form.admin.data
        if form.confirmed.data:
            user.confirmed_on = Utils.get_datetime()
            user.is_confirmed = True
        db.session.commit()
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/delete_user/<id>')
@login_required
def delete_user(id):
    # TODO: Add confirmation dialog before acting on the delete
    raise Exception('Not implemented')


@admin.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.is_authenticated and current_user.is_admin:
        form = CreateUserForm()
        if request.method == 'POST':
            if form.validate_on_submit:
                print('Form submitted')
                if form.confirmed.data:
                    confirmed_on = Utils.get_datetime()
                    user = User(
                        email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        is_admin=form.admin.data,
                        is_confirmed=True,
                        confirmed_on=confirmed_on
                    )
                else:
                    user = User(
                        email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        is_admin=form.admin.data,
                        is_confirmed=False
                    )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('admin.show_users'))
        return render_template('admin/create_user.html', form=form)
    else:
        return redirect(url_for('home.homepage'))
