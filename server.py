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

clients = {}
clients_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    username = None

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg.startswith("/setname "):
                username = msg.split(" ", 1)[1]
                with clients_lock:
                    clients[username] = conn
                print(f"[USERNAME SET] {username} for {addr}")
                continue
            
            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if username:
                if msg.startswith("@"):  # Check for direct message
                    target_user, direct_msg = msg[1:].split(" ", 1)
                    formatted_msg = f"[{timestamp}] [DM from {username}] to [{target_user}]: {direct_msg}"
                    with clients_lock:
                        if target_user in clients:
                            clients[target_user].sendall(formatted_msg.encode(FORMAT))
                        else:
                            conn.sendall(f"[ERROR] User {target_user} not found.".encode(FORMAT))
                else:
                    formatted_msg = f"[{timestamp}] [{username}] {msg}"
                    print(formatted_msg)
                    with clients_lock:
                        for client_conn in clients.values():
                            if client_conn != conn:
                                client_conn.sendall(formatted_msg.encode(FORMAT))
                    # Optionally, the server can send a broadcast message to all clients.
                    # For example, you can implement server commands to broadcast messages.
                    # Uncomment the following lines to enable server-broadcasted messages:
                    # broadcast_msg = f"[{timestamp}] [SERVER]: {msg}"
                    # for client_conn in clients.values():
                    #     client_conn.sendall(broadcast_msg.encode(FORMAT))

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        with clients_lock:
            if username in clients:
                del clients[username]
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start():
    server.listen()
    print('[SERVER STARTED]!')
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            print(f"[ERROR] Connection handling error: {e}")

start()
