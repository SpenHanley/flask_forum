from flask import render_template, url_for, redirect
from flask_login import current_user
from sqlalchemy import desc

from app.forms import CommentForm, SearchForm
from . import home
from .. import db
from ..models import SubForum, Post, User, Comment


@home.route('/')
def homepage():
    sub_forums = SubForum.query.order_by(desc('pinned'))
    return render_template(
        'home/index.html',
        title='Flask Forum',
        forums=sub_forums,
        search_form=SearchForm()
    )


@home.route('/post/<route>', methods=['GET', 'POST'])
def view_post(route):
    comments = []
    post = Post.query.filter_by(route=route).first()
    sub = SubForum.query.filter_by(id=post.sub_id).first()
    form = CommentForm()

    post_author = User.query.filter_by(id=post.author_id).first()

    post.author = post_author.username

    if form.validate_on_submit():
        comment = Comment(
            author=current_user.id,
            content=form.comment.data,
            post_id=post.id
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
                'author_id': user.id,
                'date': comment.date,
                'id': comment.id,
                'updated': comment.updated,
                'route': user.profile_route
            }
            comments.append(comm)

    return render_template(
        'home/post.html',
        post=post,
        author=post_author,
        comments=comments,
        form=form,
        sub=sub,
        search_form=SearchForm(),
        include_control=True
    )


@home.route('/sub/<route>')
def view_sub(route):
    sub = SubForum.query.filter_by(route=route).first()

    posts_arr = Post.query.filter_by(
        sub_id=sub.id
    ).order_by(desc('pinned'))

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


# TODO: Reimplement pinning sub forums
@home.route('/pin_sub/<route>', methods=['GET', 'POST'])
def pin_sub(route):
    sub = SubForum.query.filter_by(route=route).first()
    pinned = sub.pinned
    if pinned:
        pinned = False
    else:
        pinned = True
    sub.pinned = pinned
    db.session.commit()
    return redirect(url_for('home.homepage'))


# TODO: Reimplement pinning posts
@home.route('/pin_post/<route>', methods=['GET', 'POST'])
def pin_post(route):
    post = Post.query.filter_by(route=route).first()
    pinned = post.pinned
    if pinned:
        pinned = False
    else:
        pinned = True
    post.pinned = pinned
    db.session.commit()
    return redirect(url_for('home.homepage'))


# TODO: Reimplement search functionality
@home.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        term = form.search.data
        users = None
        posts = None

        print('Search term passed | {}'.format(term))

        # If the user uses the '@' symbol in the search they are looking for a user
        if term.startswith('@'):
            term = form.search.data[1:]
            users = User.query.filter(User.username.like("%" + term + "%")).all()
            print('Searched for user')
            print('Found {} users'.format(len(users)))
        else:
            posts = Post.query.filter(
                Post.title.like("%" + term + "%")
            ).all()

        subs = []
        if posts is not None:
            for post in posts:
                sub = SubForum.query.filter_by(id=post.sub_id)
                subs.append(sub)
        return render_template(
            'home/results.html',
            posts=posts,
            term=form.search.data,
            search_form=form,
            subs=subs,
            users=users
        )
    else:
        print(form.errors)
        return render_template('home/results.html', posts={}, search_form=SearchForm())
