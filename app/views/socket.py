# -*- coding: utf-8 -*-
"""
实时更新页面状态

@author: guyskk
"""
from flask_socketio import emit
from app import app, socket
from app.tasks import tasks


@app.route('/api/socket')
def show_socket():
    return app.send_static_file('socket.html')


@app.route('/api/socket/test')
def test_socket():
    socket.emit('pong', {'data': 'test!'})
    tasks.emit_test_message.delay()
    return "Emit test!"


@socket.on('ping')
def on_ping(message):
    print('received message: ' + str(message))
    emit('pong', {'data': 'I got it!'})
