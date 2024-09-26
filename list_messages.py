import socket
import threading

from websocket import send

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None
    return client

def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
            else:
                break
        except Exception as e:
            print(f"[ERROR] Error receiving message: {e}")
            break
    client.close()

def start():
    connection = connect()
    if connection is None:
        return

    # Set username
    username = input("Enter your username: ")
    send(connection, f"/setname {username}")

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(connection,), daemon=True).start()
    print("[LISTENER STARTED] Listening for messages...")

    # Keep the script running
    try:
        while True:
            pass  # Keep the main thread alive to listen for messages
    except KeyboardInterrupt:
        print("Shutting down the listener.")
        connection.close()

start()
