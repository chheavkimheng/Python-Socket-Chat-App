import threading
import socket
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue

            timestamped_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {addr}: {msg}"
            print(timestamped_msg)

            with clients_lock:
                for c in clients:
                    if c != conn:  # Prevent sending the message back to the sender
                        c.sendall(timestamped_msg.encode(FORMAT))

    except Exception as e:
        print(f"An error occurred with {addr}: {e}")
    finally:
        with clients_lock:
            clients.remove(conn)

        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start():
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        try:
            conn, addr = server.accept()
            with clients_lock:
                clients.add(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            print(f"An error occurred while accepting a connection: {e}")

start()
