from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

HOST = 'localhost'
PORT = 5555
BUFSIZ = 1024
ADDR = (HOST, PORT)



def receive_messages():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg, end="\n")
        except:
            pass

def send_message(msg):
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        print("closing")
        client_socket.close()

if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    send_message("Juan")
    receive_thread = Thread(target=receive_messages)
    receive_thread.start()
    time.sleep(5)
    send_message("HI")
    time.sleep(5)
    send_message("{quit}")
    
    