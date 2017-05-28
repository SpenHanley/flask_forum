from flask import Flask, render_template
from pymongo import MongoClient
import bson

app = Flask(__name__)


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

    return render_template('index.html', subs=subs)


@app.route('/s', methods=['GET'])
def search():
    return render_template('results.html', res=None)


@app.route('/sb/<id>')
def sub_id(id):
    subs = get_posts(id)
    sb = []
    for sub in subs:
        sub['redir'] = 'ps'
        sub['type'] = 'post'
        sub['posts'] = get_comments(bson.objectid.ObjectId(sub['_id'])).count()
        sb.append(sub)
    return render_template('index.html', subs=sb)


@app.route('/ps/<id>')
def view_post(id):
    id = bson.objectid.ObjectId(id)
    posts = db.posts.find({'_id': id}).limit(1)
    comments = get_comments(id)
    comms = []
    for comment in comments:
        comms.append(comment)
    return render_template('post.html', post=posts[0], comments=comms)


def get_posts(id):
    id = bson.objectid.ObjectId(id)
    return db.posts.find({'sub_id': id})


def get_comments(id):
    return db.comments.find({'post_id': id})


if __name__ == '__main__':
    app.run(debug=True)
