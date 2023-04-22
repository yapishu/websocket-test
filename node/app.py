from threading import Thread
import socketio
import time
import logging
import os

sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1, reconnection_delay_max=5)

auth_token = os.getenv('AUTH_TOKEN')

def periodic_send_update():
    while True:
        update = {"data": "Node status update"}
        send_update(update)
        time.sleep(8)

@sio.event
def connect():
    print('Connected to controller')

@sio.event
def disconnect():
    print('Disconnected from controller')

@sio.event
def node_update(update):
    print('Received update from controller:', update)

def send_update(update):
    print('Updating controller with',update)
    sio.emit('node_update', update, namespace='/')

def connect_to_controller():
    while True:
        try:
            sio.connect(f'ws://wscontroller:5000?token={auth_token}')
            break
        except Exception as e:
            print(f"Error connecting to controller: {e}")
            time.sleep(5)

if __name__ == '__main__':
    connect_to_controller()
    sio.start_background_task(periodic_send_update)