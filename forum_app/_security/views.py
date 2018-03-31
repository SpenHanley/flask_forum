from flask import render_template, redirect
from flask_login import login_required
from . import security


@security.route('/login')
def login():
    return render_template('_security/login')


@security.route('/logout')
def logout():
    return render_template('_security/logout')

@security.route('/register')
def register():
    return render_template('_security/register')