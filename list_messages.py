import socket
import threading

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

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(connection,), daemon=True).start()
    print("[LISTENER STARTED] Listening for messages...")

    try:
        while True:
            command = input("Enter 'list' to see messages or 'q' to quit: ")
            if command == 'q':
                break
            elif command == 'list':
                send(connection, "/list")  # Send a command to the server to list messages
    except KeyboardInterrupt:
        print("Shutting down the listener.")
    finally:
        connection.close()

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

start()
