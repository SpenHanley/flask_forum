from flask import render_template
from flask_login import login_required
from ..models import Post, SubForum

from . import home


@home.route('/')
def homepage():
    return render_template('home/index.html', title='Flask Forum')


@home.route('/acc')
@login_required
def dash():
    return render_template('home/dash.html', title='Flask Forum')


@home.route('/post/<id>')
def view_post(id):
    post = Post.query.get(int(id)).first()
    return render_template('home/post.html', post=post)


@home.route('/sb/<id>')
def view_sub(id):
    sub = SubForum.query.get(int(id))
    return render_template('home/sub.html', sub=sub)