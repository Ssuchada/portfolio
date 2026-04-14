# node.py
import socket
import threading
import random
import uuid
from config import HOST, BASE_PORT, BUFFER_SIZE, NEIGHBORS, FORWARD_PROBABILITY, TTL

PORT = BASE_PORT
neighbor_table = set(NEIGHBORS)

seen_messages = set()

# ________________________________________
def handle_incoming(conn, addr):
    try:
        data = conn.recv(BUFFER_SIZE).decode()

        # format: msg_id|message|ttl
        msg_id, msg, ttl = data.split('|')
        ttl = int(ttl)

        if msg_id in seen_messages:
            return
        seen_messages.add(msg_id)

        print(f"[NODE {PORT}] Received from {addr}: {msg} (TTL={ttl})")

        # forward
        if ttl > 0 and random.random() < FORWARD_PROBABILITY:
            forward_message(msg_id, msg, ttl - 1)

    except Exception as e:
        print(f"[NODE {PORT}] Error: {e}")
    finally:
        conn.close()

# ________________________________________
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"[NODE {PORT}] Listening for neighbors...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_incoming, args=(conn, addr), daemon=True).start()

# ________________________________________
def forward_message(msg_id, message, ttl):
    for peer_port in neighbor_table:

        if peer_port == PORT:
            continue

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, peer_port))
            s.sendall(f"{msg_id}|{message}|{ttl}".encode())
            s.close()
        except Exception:
            print(f"[NODE {PORT}] Peer {peer_port} unreachable")

# ________________________________________
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()

    while True:
        msg = input("Message: ")

        msg_id = str(uuid.uuid4())

        forward_message(msg_id, msg, TTL)