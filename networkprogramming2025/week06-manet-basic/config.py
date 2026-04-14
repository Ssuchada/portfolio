#Step 0: Shared Configuration
# config.py
HOST = "127.0.0.1"
BUFFER_SIZE = 1024
BASE_PORT = 7002
NEIGHBORS = [7001]
FORWARD_PROBABILITY = 0.5  # 50% chance to forward
TTL = 3  # Max hops for message
