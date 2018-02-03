from flask import session, flash
from flask_socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    flash(message)
    room = session.get('room')
    join_room(room)
    print('Joined')
    emit('status', {'msg': session.get('name') + ' has entered the room'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    flash('Text', message)
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    flash(message)
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room'}, room=room)
