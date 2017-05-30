from flask import Flask, render_template, g, redirect, request, session
from datetime import datetime
from pymongo import MongoClient
from utils import Utils
from config import Config
from functools import wraps
import random
import pymongo
import string

conf = Config()

app = Flask(__name__)
key = None
with open('keyfile', 'r') as kf:
    key = kf.read()

app.secret_key = key

client = MongoClient(conf.config.get('mongo_db', 'host'), int(conf.config.get('mongo_db', 'port')))
print(conf.config.get('mongo_db', 'db_name'))
db = client[conf.config.get('mongo_db', 'db_name')]
db = client['forum']

utils = Utils(db)


def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(length))


def validate_token(f):
    @wraps(f)
    def wrapper(existing_token, *args, **kwargs):
        if 'token' in session:
            if session['token'] != existing_token:
                print('User token is invalid')
            else:
                print('User token is valid')
        else:
            session['token'] = random_string(32)




@app.route('/')
def hello_world():
    sub_coll = db['subs']
    subs_coll = sub_coll.find().sort("pinned", pymongo.DESCENDING)
    subs = []
    for sub in subs_coll:
        sub['modified'] = sub['modified']
        sub['id'] = sub['route']
        sub['redir'] = 'sb'
        sub['type'] = 'sub'
        sub['pinned_sub'] = 'pinned' in sub
        posts = utils.get_post_count(sub['_id'])
        posts_coll = posts.count()
        sub['posts'] = posts_coll
        subs.append(sub)
    return render_template('index.html', subs=subs)


@app.route('/s/', methods=['GET'])
def search():
    if request.method == 'GET':
        resp = utils.search_db(request.args)
        return render_template('results.html', posts=resp)


@app.route('/acc/')
def account():
    if session['user'] is None:
        return redirect('/lg/')
    else:
        return render_template('account.html')


@app.route('/sb/<id>')
def sub_id(id):
    posts = utils.get_posts(id)
    ps = []
    curr = db.subs.find({'route': id}).limit(1)[0]
    for post in posts:
        post['redir'] = 'ps'
        post['pinned_post'] = 'pinned' in post
        post['posts'] = utils.get_comments(utils.convert_to_object_id(post['_id'])).count()
        post['modified'] = post['timestamp']
        post['comments'] = utils.get_comments(post['_id']).count()
        ps.append(post)
    return render_template('post_list.html', sub=curr, posts=ps)


@app.route('/pf/<id>')
def create_post(id):
    if session.get('user'):
        prev = db['subs'].find({'_id': utils.convert_to_object_id(id)}).limit(1)[0]
        return render_template('post_form.html', allow_anon=conf.config.getboolean('ui_ctl', 'AllowAnonymous'), selected=prev)
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
    post = db['posts'].find({'route': id}).limit(1)[0]
    author = utils.get_author(post['author'])

    print(post['anonymous'])
    if post['anonymous']:
        if session.get('user'):
            author['_id'] = utils.convert_to_object_id(author['_id'])
            sess_id = utils.convert_to_object_id(utils.convert_from_json_id(session['id']))
            if session['user']['admin']:
                post['author'] = author['username'] + " as Anonymous"
            elif sess_id == author['_id']:
                post['author'] = "You as Anonymous"
        else:
            print('User is neither an admin not the author')
            post['author'] = "Anonymous"
    else:
        post['author'] = author['username']

    post['timestamp'] = post['timestamp']
    sub = db['subs'].find({'_id': utils.convert_to_object_id(post['sub_id'])}).limit(1)[0]
    comments = utils.get_comments(post['_id'])
    cs = []
    for comment in comments:
        comment['timestamp'] = comment['timestamp']
        comment['author'] = utils.get_author(comment['author'])['username']
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


@app.route('/cs', methods=['GET', 'POST'])
def rt_create_sub():
    if request.method == 'POST':
        create_sub(request.form)
        return redirect('/')
    else:
        return render_template('create_sub.html')


@app.route('/pn/<id>')
def pin_sub(id):
    id = utils.convert_to_object_id(id)
    sub = db['subs'].find({'_id': id}).limit(1)[0]
    if 'pinned' in sub:
        db['subs'].update_one({'_id': sub['_id']}, {"$unset": {'pinned': ""}})
        return redirect('/')
    else:
        db['subs'].update_one({'_id': sub['_id']}, {"$set": {'pinned': True}})
        return redirect('/')


@app.route('/pnp/<id>')
def pin_post(id):
    post = db['posts'].find({'route': id}).limit(1)[0]
    sub = db['subs'].find({'_id': post['sub_id']}).limit(1)[0]
    if 'pinned' in post:
        db['posts'].update_one({'_id': post['_id']}, {"$unset": {'pinned': ""}})
        return redirect('/sb/' + str(sub['route']))
    else:
        db['posts'].update_one({'_id': post['_id']}, {"$set": {'pinned': True}})
        return redirect('/sb/' + str(sub['route']))


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
        admin = 'admin' in user
        if user['password'] == password:
            u = {
                'username': user['username'],
                'email': user['email'],
                'admin': admin
            }
            session['user'] = u
            session['id'] = utils.convert_to_json_id(user['_id'])
            return True
        else:
            return False
    else:
        return False


def add_post(req):
    # Still need to check if all of the fields have been completed
    post_title = req['title']
    keywords = req['title'].split(' ')
    post_text = req['content']
    post_anon = 'anonymous' in req
    sub = utils.convert_to_object_id(req['sub'])
    sb = db['subs'].find({'_id': sub})
    timestamp = datetime.timestamp(datetime.utcnow())
    db['subs'].update_one({'_id': sub}, {"$set": {"modified": timestamp}})
    post_author = utils.convert_to_object_id(utils.get_author_id(session['user']['username']))
    post = {
        'title': post_title,
        'content': post_text,
        'author': post_author,
        'timestamp': timestamp,
        'sub_id': sub,
        'anonymous': post_anon,
        'route': utils.generate_random_path(),
        'keywords': keywords
    }

    resp = db['posts'].insert(post)


def add_comment(req):
    # Still need to check if all of the fields have been completed
    author = utils.get_author_id(session['user']['username'])
    author = utils.convert_to_object_id(author)
    timestamp = datetime.timestamp(datetime.utcnow())
    post_id = utils.convert_to_object_id(req['post_id'])
    comment_text = req['comment']
    comment = {
        'author': author,
        'timestamp': timestamp,
        'post_id': post_id,
        'comment': comment_text
    }
    resp = db['comments'].insert(comment)


def create_sub(req):
    title = req['title']
    description = req['desc']
    mod = datetime.timestamp(datetime.utcnow())
    sub = {
        'title': title,
        'description': description,
        'modified': mod,
        'route': utils.generate_random_path()
    }
    resp = db['subs'].insert(sub)


if __name__ == '__main__':
    app.run(debug=True)
