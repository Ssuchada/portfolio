# Step 1: Create Broadcast Sender
# broadcaster.py
import socket
from config import BROADCAST_IP, PORT, BUFFER_SIZE

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# CRITICAL: Enable broadcast on this socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Send message to broadcast address
message = "DISCOVERY: Who is online?"
sock.sendto(message.encode(), (BROADCAST_IP, PORT))

print("[BROADCASTER] Message sent")
sock.close()