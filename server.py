import socket
import threading
import requests


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Error:", e)
        return None

local_ip = get_local_ip()

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to retrieve IP address:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None

public_ip = get_public_ip()



HOST = get_local_ip()
PORT = 8081



def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            print(f"Received message from {client_address}: {message}")

            broadcast(message)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")

    finally:
        if client_socket in clients:
            clients.remove(client_socket)

    print(f"Connection from {client_address} closed")
    client_socket.close()

def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}\nfor www connections: {public_ip}")

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
