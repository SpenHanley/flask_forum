import random, string, os

if not os.path.isfile('s.key'):
    SECRET_KEY = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(64))
    with open('s.key', 'w') as key:
        key.write(SECRET_KEY)
else:
    with open('s.key', 'r') as key:
        SECRET_KEY = key.read()

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/fforum_db'
