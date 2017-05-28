from flask import Flask, render_template, g, redirect, request
from pymongo import MongoClient
import bson

app = Flask(__name__)

global err
client = MongoClient('localhost', 27017)
db = client['forum']


@app.route('/')
def hello_world():
    sub_coll = db['subs']
    subs_coll = sub_coll.find()
    subs = []
    for sub in subs_coll:
        print()
        sub['id'] = sub['_id']
        sub['redir'] = 'sb'
        sub['type'] = 'sub'
        posts_coll = get_posts(bson.objectid.ObjectId(sub['_id'])).count()
        sub['posts'] = posts_coll
        subs.append(sub)

    return render_template('index.html', subs=subs, sub=None, user=g.get('user', None))


@app.route('/s', methods=['GET'])
def search():
    return render_template('results.html', res=None)


@app.route('/acc/')
def account():
    if g.get('user', None) is None:
        return redirect('/lg/')
    else:
        return render_template('account.html', user=g.get('user', None))


@app.route('/sb/<id>')
def sub_id(id):
    subs = get_posts(id)
    sb = []
    curr = db.subs.find({'_id': bson.objectid.ObjectId(id)}).limit(1)
    for sub in subs:
        sub['redir'] = 'ps'
        sub['type'] = 'post'
        sub['posts'] = get_comments(bson.objectid.ObjectId(sub['_id'])).count()
        sb.append(sub)
    return render_template('index.html', subs=sb, sub=curr[0], post=None, user=g.get('user', None))


@app.route('/ps/<id>')
def view_post(id):
    id = bson.objectid.ObjectId(id)
    posts = db.posts.find({'_id': id}).limit(1)
    comments = get_comments(id)
    comms = []
    sub = db.subs.find({'_id': bson.objectid.ObjectId(posts[0]['sub_id'])}).limit(1)
    for comment in comments:
        comms.append(comment)
    sub[0]['title'] = sub[0]['title'].replace("\ ", "\_")
    print(sub[0]['title'])
    return render_template('post.html', post=posts[0], comments=comms, sub=sub[0], user=g.get('user', None))


@app.route('/reg/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if register_user(request.form):
            return redirect('/')
        else:
            err = 'Failed to register'
            return redirect('/reg/')
    else:
        return render_template('register.html', sub=None, user=g.get('user', None))

@app.route('/lg/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if login(request.form):
            return redirect('/')
    else:
        return render_template('login.html', user=g.get('user', None), sub=None)


def get_posts(id):
    id = bson.objectid.ObjectId(id)
    return db.posts.find({'sub_id': id})


def get_comments(id):
    return db.comments.find({'post_id': id})


def register_user(req):
    print(req)
    username = req['username']
    password = req['password']
    email = req['email']
    conf = req['confirm']
    if conf != email:
        return False
    else:
        users = db['users']
        user = users.find({'username': username}).count()
        print(user)
        if user > 0:
            return False
        else:
            resp = users.insert({'username':username, 'password': password, 'email': email})
            print(resp)
            return True

def login(req):
    username = req['username']
    password = req['password']
    user = db['users'].find({'username': username}).limit(1)
    if user[0]['password'] == password:
        g.set('user', user)
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)
