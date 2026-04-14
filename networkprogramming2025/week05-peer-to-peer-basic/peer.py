# peer.py
import socket
import threading
import sys
from config import HOST, BASE_PORT, BUFFER_SIZE

peer_id = int(sys.argv[1])
PORT = BASE_PORT + peer_id

# ________________________________________
# Step 2: Listener Thread
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[PEER {peer_id}] Listening on {PORT}")

    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE)

        if data:
            print(f"\n[PEER {peer_id}] From {addr}: {data.decode()}")

        conn.close()

# ________________________________________
# Step 3: Sender Function
def send_message(target_peer_id, message):
    target_port = BASE_PORT + target_peer_id

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, target_port))
        sock.sendall(message.encode())
        sock.close()
    except Exception as e:
        print(f"[PEER {peer_id}] Error sending: {e}")

# ________________________________________
# Step 4: Run Listener + Send Message
threading.Thread(target=listen, daemon=True).start()

# main loop
while True:
    try:
        target = int(input("Send to peer ID: "))
        msg = input("Message: ")
        send_message(target, msg)
    except Exception as e:
        print(f"[PEER {peer_id}] Input error: {e}")