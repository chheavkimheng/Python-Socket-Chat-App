import socket
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

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
    print("[CLIENT STARTED] You can start sending messages.")

    while True:
        msg = input("Message (q for quit, @username message for DM): ")
        if msg == 'q':
            send(connection, DISCONNECT_MESSAGE)
            print('Disconnected')
            break
        send(connection, msg)

start()
