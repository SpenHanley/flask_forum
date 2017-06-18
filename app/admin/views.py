from flask import flash, redirect, render_template, url_for, request

from . import admin
from ..models import User
from ..auth.forms import EditUserForm
from .. import db
from utils import Utils


@admin.route('')
def homepage():
    return render_template('admin/index.html')


@admin.route('/usr')
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@admin.route('/editu/<id>')
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


@admin.route('/delu/<id>')
def delete_user(id):
    # TODO: Add confirmation dialog before acting on the delete
    pass
