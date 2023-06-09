from flask import Flask, request
from flask_socketio import SocketIO, emit, disconnect
import logging
import json
import os
import time

app = Flask(__name__)
auth_token = os.getenv('AUTH_TOKEN')
app.config['SECRET_KEY'] = auth_token
socketio = SocketIO(app, cors_allowed_origins='*')

def authenticate(token):
    return token == auth_token

@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    nodename = request.args.get('node')
    if not authenticate(token):
        disconnect()
    else:
        print(f"Node {nodename} connected")

@socketio.on('ctl_update')
def ctl_update(update):
    nodename = request.args.get('node')
    print(f'Received update from {nodename}:', update)

def node_state():
    data = {
        'test1': 'data1',
        'test2': 'data2',
        'test3': {
            '2test1': '2data1'
        }
    }
    return data

def nodes(nodes_data):
    with app.test_request_context():
        print('Pushing update')
        socketio.emit('node_update', nodes_data, namespace='/')

def periodic_push_nodes():
    while True:
        nodes_data = node_state()
        nodes(nodes_data)
        time.sleep(5)

if __name__ == '__main__':
    socketio.start_background_task(periodic_push_nodes)
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
