from flask import Flask
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)
clients = {}  # Dictionary to hold client ID and timestamp

# Function to send ping and start a timeout timer
def ping_clients():
    while True:
        socketio.sleep(60)  # Wait for 1 minute before sending the next ping
        for client_id, timer in clients.items():
            emit('ping', {'message': 'Are you alive?'}, room=client_id)
            threading.Timer(60, check_timeout, [client_id]).start()  # Set a 1-minute timeout

# Function to check if the client responded within 1 minute
def check_timeout(client_id):
    if clients.get(client_id, None) and clients[client_id]['response'] == False:
        # Client didn't respond, remove them from the list
        print(f"Client {client_id} did not respond. Removing from list.")
        clients.pop(client_id)

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    clients[client_id] = {'response': True}  # Add client to the list
    print(f"Client {client_id} connected.")

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    clients.pop(client_id, None)
    print(f"Client {client_id} disconnected.")

@socketio.on('pong')  # Response from client to ping
def handle_pong(data):
    client_id = request.sid
    if client_id in clients:
        clients[client_id]['response'] = True  # Mark the client as active
        print(f"Client {client_id} is still alive.")


socketio.start_background_task(ping_clients)
socketio.run(app)
