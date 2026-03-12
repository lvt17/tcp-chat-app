import socket
import threading
import json
#from shared.protocol import *

"""
!!! watching the explanation in DOCX/research/server_explain.md !!!
"""

#define
SERVER_IP='0.0.0.0'
PORT=8000

#setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))
server.listen()
print(f"[LISTENING] {SERVER_IP}:{PORT}") #show server IP and port

def handleClient(client_socket, addr):
    print(f"[CONNECTED] {addr}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data: #client out
                print(f"[DISCONNECT] {addr}")
                break

            msg = data.decode("utf-8") #client message send
            print(f"[{addr}] {msg}")

            reply = f"Server received: {msg}" #server message reply
            client_socket.send(reply.encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        client_socket.close()

#client processing
while True:
    client_socket, addr = server.accept()
    print(f"[NEW CONNECT] {addr}")
    
    #create new thread for this client
    thread = threading.Thread(target=handleClient, args=(client_socket, addr))
    thread.start()