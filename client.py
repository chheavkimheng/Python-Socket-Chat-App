import socket
import time
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, username, msg):
    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [{username}] {msg}".encode(FORMAT)
    client.send(message)

def start():
    username = input('Enter your username: ')
    answer = input('Would you like to connect to the server (yes/no)? ')
    if answer.lower() != 'yes':
        return

    try:
        connection = connect()
        print("Connected to the server.")
        
        while True:
            msg = input("Message (q for quit): ")

            if msg == 'q':
                break

            send(connection, username, msg)

        send(connection, username, DISCONNECT_MESSAGE)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print('Disconnected')

start()
