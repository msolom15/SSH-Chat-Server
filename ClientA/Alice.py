import paramiko
import threading


HOST = input("Please Enter Server IP: ")
PORT = input("Please Enter Port Number: ")
USERNAME = input("Please Enter Username: ")

# runs forever and reads in coming messages and prints them when they arrive
def recv_loop(chan):
    while True:
        try:
            data = chan.recv(1024)
            if not data:
                break
            print("\n" + data.decode(), end="")
        except:
            break
# loads the private key
private_key = paramiko.RSAKey.from_private_key_file("ClientA/private_key.pem")
# SSH setup and automatically accepts a new server hostkey
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connects to the SSH server
client.connect(
    HOST,
    port=PORT,
    username=USERNAME,
    pkey=private_key,
    look_for_keys=False,
    allow_agent=False
)
# opens an SSH session
chan = client.get_transport().open_session()

# allows client to send and recieve messages by giving each client their own thread
threading.Thread(target=recv_loop, args=(chan,), daemon=True).start()

#send the messages
print("\n")
while True:
    Alice = input()
    chan.send(Alice + "\n")
