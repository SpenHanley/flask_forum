from datetime import datetime
from bson.json_util import dumps, loads
import pymongo
import string
import random
import bson


class Utils:
    def __init__(self, db):
        self.db = db

    def get_posts(self, id):
        new_id = self.db.subs.find({'route': id}).limit(1)[0]['_id']
        return self.db.posts.find({'sub_id': new_id}).sort("pinned", pymongo.DESCENDING)

    def get_post_count(self, id):
        return self.db.posts.find({'sub_id': self.convert_to_object_id(id)})

    def get_comments(self, id):
        return self.db.comments.find({'post_id': self.convert_to_object_id(id)})

    def get_author(self, id):
        return self.db['users'].find({'_id': self.convert_to_object_id(id)}).limit(1)[0]

    def get_author_id(self, username):
        return self.db['users'].find({'username': username}).limit(1)[0]['_id']

    def get_timestamp(self):
        return datetime.timestamp(datetime.utcnow())

    def convert_timestamp(self, ts):
        return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")

    def convert_to_object_id(self, id):
        return bson.objectid.ObjectId(id)

    def convert_to_json_id(self, id):
        return dumps(id)

    def convert_from_json_id(self, id):
        return loads(id)

    def generate_random_path(self):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))

    def search_db(self, args):
        posts = self.db['posts'].find()
        resp = []
        for post in posts:
            for keyword in post['keywords']:
                if args['kw'].lower() == keyword.lower():
                    post['modified'] = self.convert_timestamp(post['timestamp'])
                    resp.append(post)
        return resp
