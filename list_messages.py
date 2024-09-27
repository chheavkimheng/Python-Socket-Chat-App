import socket
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def start():
    try:
        connection = connect()
        print("Listening for messages...")
        while True:
            msg = connection.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

start()
