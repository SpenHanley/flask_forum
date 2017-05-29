from flask import Flask, render_template, g, redirect, request, session
from datetime import datetime
import time
from pymongo import MongoClient
import bson

app = Flask(__name__)
key = None
with open('/home/spen/keyfile', 'r') as kf:
    key = kf.read()

app.secret_key = key

global err
client = MongoClient('localhost', 27017)
db = client['forum']


@app.route('/')
def hello_world():
    sub_coll = db['subs']
    subs_coll = sub_coll.find()
    subs = []
    for sub in subs_coll:
        sub['modified'] = convert_timestamp(sub['modified'])
        sub['id'] = sub['_id']
        sub['redir'] = 'sb'
        sub['type'] = 'sub'
        posts_coll = get_posts(sub['_id']).count()
        sub['posts'] = posts_coll
        subs.append(sub)
    return render_template('index.html', subs=subs)


@app.route('/s', methods=['GET'])
def search():
    return render_template('results.html')


@app.route('/acc/')
def account():
    if session['user'] is None:
        return redirect('/lg/')
    else:
        return render_template('account.html')


@app.route('/sb/<id>')
def sub_id(id):
    posts = get_posts(id)
    ps = []
    curr = db.subs.find({'_id': convert_id(id)}).limit(1)[0]
    for post in posts:
        post['redir'] = 'ps'
        post['posts'] = get_comments(convert_id(post['_id'])).count()
        post['modified'] = convert_timestamp(post['timestamp'])
        post['comments'] = get_comments(post['_id']).count()
        ps.append(post)
    return render_template('post_list.html', sub=curr, posts=ps)


@app.route('/pf/')
def create_post():
    if session.get('user'):
        subs = db['subs'].find()
        return render_template('post_form.html', subs=subs)
    else:
        return redirect('/lg/')


@app.route('/cp', methods=['GET', 'POST'])
def submit_post():
    if request.method == 'POST':
        add_post(request.form)
        return redirect('/')
    else:
        return redirect('/')


@app.route('/ps/<id>/')
def view_post(id):
    post = db['posts'].find({'_id': convert_id(id)}).limit(1)[0]
    post['author'] = get_author(post['author'])['username']
    post['timestamp'] = convert_timestamp(post['timestamp'])
    sub = db['subs'].find({'_id': convert_id(post['sub_id'])}).limit(1)[0]
    comments = get_comments(id)
    cs = []
    for comment in comments:
        comment['timestamp'] = convert_timestamp(comment['timestamp'])
        comment['author'] = get_author(comment['author'])['username']
        cs.append(comment)
    return render_template('post.html', post=post, comments=cs, sub=sub)


@app.route('/reg/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if register_user(request.form):
            return redirect('/')
        else:
            err = 'Failed to register'
            return redirect('/reg/')
    else:
        return render_template('register.html')


@app.route('/lg/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if user_login(request.form):
            return redirect('/')
        else:
            return redirect('/lg/')
    else:
        return render_template('login.html')


@app.route('/lo/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/cm/', methods=['GET', 'POST'])
def comment():
    print(request.method)
    if request.method == 'POST':
        add_comment(request.form)
        return redirect(request.form['path'])
    else:
        return redirect(request.form['path'])


def register_user(req):
    print(req)
    username = req['username']
    password = req['password']
    email = req['email']
    conf = req['confirm']
    if conf != email:
        return False
    else:
        if len(username.strip()) > 0:
            users = db['users']
            user = users.find({'username': username}).count()
            print(user)
            if user > 0:
                return False
            else:
                resp = users.insert({'username': username, 'password': password, 'email': email})
                print("ID of inserted record: " + resp)
                return True
        else:
            return False


def user_login(req):
    username = req['username']
    password = req['password']
    users = db['users'].find({'username': username}).limit(1)
    if users.count() > 0:
        user = users[0]
        if user['password'] == password:
            u = {
                'username': user['username'],
                'email': user['email']
            }
            session['user'] = u
            return True
        else:
            return False
    else:
        return False


def add_post(req):
    # Still need to check if all of the fields have been completed
    post_title = req['title']
    post_text = req['content']
    sub = convert_id(req['sub'])
    post_author = convert_id(get_author_id(session['user']['username']))
    post = {
        'title': post_title,
        'content': post_text,
        'author': post_author,
        'timestamp': datetime.timestamp(datetime.utcnow()),
        'sub_id': sub
    }

    resp = db['posts'].insert(post)


def add_comment(req):
    # Still need to check if all of the fields have been completed
    author = get_author_id(session['user']['username'])
    author = convert_id(author)
    timestamp = datetime.timestamp(datetime.utcnow())
    post_id = convert_id(req['post_id'])
    comment_text = req['comment']
    comment = {
        'author': author,
        'timestamp': timestamp,
        'post_id': post_id,
        'comment': comment_text
    }
    resp = db['comments'].insert(comment)


def get_posts(id):
    return db.posts.find({'sub_id': convert_id(id)})


def get_comments(id):
    return db.comments.find({'post_id': convert_id(id)})


def get_author(id):
    return db['users'].find({'_id': convert_id(id)}).limit(1)[0]


def get_author_id(username):
    return db['users'].find({'username': username}).limit(1)[0]['_id']


def convert_timestamp(ts):
    return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")


def convert_id(id):
    return bson.objectid.ObjectId(id)


if __name__ == '__main__':
    app.run(debug=True)
