import os

from app import create_app
from flask_socketio import SocketIO

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
socket_io = SocketIO(app)


if __name__ == '__main__':
    socket_io.run(app)
