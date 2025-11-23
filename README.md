# SSH Chat System --- Secure Paramiko-Based Messaging

------------------------------------------------------------------------

## 📘 Overview

This project implements a secure, SSH-based real‑time chat system using
**Python** and **Paramiko**.\
Instead of traditional sockets, the chat uses encrypted SSH channels for
communication, providing:

-   Public‑key authentication
-   End‑to‑end encrypted message transport
-   Multi‑client communication
-   Real‑time message broadcasting

The system includes two example clients (Alice & Bob), a server, and an
RSA key generation utility.

------------------------------------------------------------------------

## 📁 Project Structure

    server.py                 # SSH chat server (public‑key authentication)
    Alice.py                  # Alice client implementation
    Bob.py                    # Bob client implementation
    keygen.py                 # RSA key generator script

    /ClientA/private_key.pem   # Alice’s private key
    /ClientB/private_key.pem   # Bob’s private key
    Alicepublickey.pem         # Alice’s public key
    Bobpublickey.pem           # Bob’s public key

------------------------------------------------------------------------

## 🛠 Approach

1.  **SSH Transport Instead of Raw Sockets**\
    The project uses Paramiko's SSH `Transport` and `Channel` objects,
    allowing secure, encrypted connections without building a
    cryptographic layer manually.

2.  **Public-Key Authentication**\
    Each client supplies a private key, and the server validates it
    against a stored public key.

3.  **Threaded Message Handling**
    -   The server starts a thread for every connected client.
    -   Clients use a thread to continuously read incoming messages.
    -   The main thread handles message input and sending.

4.  **Broadcast System**\
    The server distributes messages to all clients except the sender,
    tagging them with the sender's chosen display name.

------------------------------------------------------------------------

## ⚠ Challenges Faced

### 1. **Managing Public-Key Authentication**

Mapping usernames to correct public keys required building a custom
loader and validation logic.

### 2. **Handling Multiple Clients Simultaneously**

Using threads safely without cross‑talk or crashes required careful
channel handling.

### 3. **Cross‑Platform Paramiko Behavior**

Ensuring Paramiko worked reliably on different systems involved
adjusting key‑loading behavior and disabling agent/keyfile auto‑search.

------------------------------------------------------------------------

## ✅ How These Challenges Were Overcome

### ✔ Custom Public-Key Loader

A helper function was built to read OpenSSH public-key files and convert
them into Paramiko RSAKey objects.

### ✔ Threaded Communication Model

The server uses one thread per client, and clients use a separate
receiving thread: - Prevents blocking behavior
- Allows full-duplex chat
- Ensures messages arrive in real time

### ✔ Explicit SSH Connection Controls

Using:

``` python
look_for_keys=False
allow_agent=False
```

ensured consistency and prevented unexpected authentication attempts.

------------------------------------------------------------------------

## ▶ How to Run the Project

### **1. Install Dependencies**

    pip install paramiko

### **2. Generate Keys for Alice and Bob**

    python keygen.py

### **3. Start the Chat Server**

    python server.py

Server listens on:

    0.0.0.0:2200

### **4. Run a Client (Alice or Bob)**

#### Alice:

    python Alice.py

#### Bob:

    python Bob.py

Each client will be prompted for Server IP which is **127.0.0.1**
- Port number: **2200**
- Username: **Alice** for Alice.py and **Bob** for Bob.py

### **5. Start Chatting**

Type messages in one client---they appear instantly in others.

------------------------------------------------------------------------
