import socket
import threading

SERVER_IP='127.0.0.1'
PORT=8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
print("[CONNECTED]")

def recieve():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print("\n[]SERVER", data.decode("utf-8"))
        except:
            break

threading.Thread(target=recieve, daemon=True).start()

while True:
    msg = input("YOU: ")
    if msg.lower() == "q":
        break
    client.send(msg.encode("utf-8"))
    
client.close()