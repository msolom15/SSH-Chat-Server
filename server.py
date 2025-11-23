import socket
import threading
import paramiko
import base64

# Chat Servers identity key
SERVER_KEY = paramiko.RSAKey.generate(2048)

# Loads the public key
def pubkeyload(name: str):
    with open(name, "r") as f:
        parts = f.read().strip().split()
        key_data = parts[1]
        decoded = base64.b64decode(key_data)
        return paramiko.RSAKey(data=decoded)

# List of connected clients and mappings of username to public keys
CLIENTS = []
AUTHORIZED_KEYS = {
    "Alice": pubkeyload("Alicepublickey.pem"),
    "Bob":   pubkeyload("Bobpublickey.pem"),
} 

# Handles auth and channel requests in paramiko 
class ChatServer(paramiko.ServerInterface):
    def check_auth_publickey(self, username, key):
        if username not in AUTHORIZED_KEYS:
            return paramiko.AUTH_FAILED
        
        allowed_key = AUTHORIZED_KEYS[username]

        if key == allowed_key:
            return paramiko.AUTH_SUCCESSFUL
        
        return paramiko.AUTH_FAILED
    

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

# Brodcast a senders message to other users besides the senders
def broadcast(sender, message):
    """Send a message to all other clients."""
    for c in CLIENTS:
        if c != sender:
            try:
                c.send(message)
            except:
                pass

#handles the messages for each client and brodcast them
def client_channel(chan):

    chan.send("Enter the name you would like to appear in chat: ")
    id = chan.recv(1024).decode().strip()
    chan.send(f"Welcome, {id}!\n".encode())

    CLIENTS.append(chan)
    chan.send("Connected! Type messages...\n")
    
# waits for incoming messages and attaches their chosen name then brodcast it to them
    try:
        while True:
            data = chan.recv(1024)
            if not data:
                break
            msg = data.decode().rstrip()
            broadcast(chan, f"[{id}] {msg}\n")
    finally:
        CLIENTS.remove(chan)
        chan.close()

#server config
def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 2200))
    sock.listen(100)
    print("SSH Chat Server is now up . . .")

    while True:
        client, addr = sock.accept()
        print("New connection:", addr)

        transport = paramiko.Transport(client)
        transport.add_server_key(SERVER_KEY)

        server = ChatServer()
        transport.start_server(server=server)

        chan = transport.accept()
        if chan is None:
            continue

        threading.Thread(target=client_channel, args=(chan,), daemon=True).start()


start_server()
