from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

users = []

HOST = 'localhost'
PORT = 5555
BUFSIZ = 1024  # Byte limit for each message
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

class User:
    def __init__(self, client, addr):
        self.client = client
        self.addr = addr
        self.name = None


def accept_connections():
    while True:
        client, addr = SERVER.accept() # Getting new connections
        print(f"New user connected from {addr}")
        client.send(bytes("Greeting, you are connected, now type ur name and press enter!\n", "utf8"))
        new_user = User(client, addr)
        Thread(target=handle_user, args=(new_user,)).start()

def handle_user(user):
    client = user.client
    name = client.recv(BUFSIZ).decode("utf8")
    user.name = name
    client.send(bytes(f"Welcome {name}\n", "utf8"))
    broadcast(bytes(f"{name} has joined the chat!", "utf8"))
    users.append(user)
    
    # Infinite loop for listen client message
    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{quit}", "utf8"):
            client.close()
            users.remove(user)
            broadcast(bytes(f"{name} has left the chat.\n", "utf8"))
            break
        else:
            broadcast(msg, name+": ")
            
def broadcast(msg, prefix=""):
    for user in users:
        try:
            user.client.send(bytes(prefix, "utf8")+msg)
        except:
            pass


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
