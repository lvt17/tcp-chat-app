import socket
import threading

PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.45.123"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    client.send(msg.encode(FORMAT))

def receive():
    while True:
        try:
            response = client.recv(1024).decode(FORMAT)
            if response:
                print(f"{response}")
        except:
            break

# Tạo thread nhận dữ liệu
threading.Thread(target=receive, daemon=True).start()

while True:
    mess = input("Bạn: ")
    send(mess)