import socket
import threading
import os

# Setting up the server
HOST = 'localhost'
PORT = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Inicialize rooms
rooms = {}

# Define broadcast
def broadcast(room_name, message):
    for client in rooms[room_name]:
        if isinstance(message, str):
            message = message.encode()
        client.send(message)

# Send message
def send_message(client_name, room_name, client):
    while True:
        message = client.recv(1024)
        message = f'{client_name}: {message.decode()}\n'
        broadcast(room_name, message)

# Inicialize the server
while True:
    client, addr = server.accept()
    client.send(b'room')
    room_name = client.recv(1024).decode()
    client_name = client.recv(1024).decode()
    if room_name not in rooms.keys():
        rooms[room_name] = []
    rooms[room_name].append(client)
    print(f'{client_name} se conectou na sala {room_name}! INFO: {addr}')
    broadcast(room_name, f'{client_name} entrou na sala!\n')
    thread = threading.Thread(target=send_message, args=(client_name, room_name, client))
    thread.start()