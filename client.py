import socket
import threading
import os
import time

done = False
username = input("Enter your username: ")

SERVER_HOST = input("Enter the server ip address: ")
SERVER_PORT = 8081  

def receive_messages():
    global done
    while not done:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            if message == "quit":
                done = True
                print("Are you sure you want to quit?\n")
        except:
            print("An error occurred while receiving messages.")
            client_socket.close()
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_HOST, SERVER_PORT))
print("Connected to server.")

time.sleep(1)

os.system('cls')

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while not done:
    message = input()
    client_socket.send((username + ": " + message).encode('utf-8'))
