import socket
import threading
import json
import datetime

SERVER_IP=''
PORT=8000
"""
!!! watching the explanation in DOCX/research/prototype_explain !!!
"""
client = None
username = None

def login(username):
    msg = {
        "type": "LOGIN",
        "username": username,
        "timestamp": datetime.datetime.now().isoformat()
    }
    client.send(json.dumps(msg).encode("utf-8"))

def join(username):
    msg = {
        "type": "JOIN",
        "username": username,
        "timestamp": datetime.datetime.now().isoformat()
    }
    client.send(json.dumps(msg).encode("utf-8"))

def chat(username, content):
    msg = {
        "type": "CHAT",
        "sender": username,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat()
    }
    client.send(json.dumps(msg).encode("utf-8"))

def private(sender, receiver, content):
    msg = {
        "type": "PRIVATE",
        "sender": sender,
        "receiver": receiver,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat()
    }
    client.send(json.dumps(msg).encode("utf-8"))

def leave(username):
    msg = {
        "type": "LEAVE",
        "username": username,
        "timestamp": datetime.datetime.now().isoformat()
    }
    client.send(json.dumps(msg).encode("utf-8"))


def recieve_loop():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("[DISCONNECT] Server closed connection")
                break
            text = data.decode("utf-8")
            try:
                msg = json.loads(text)
                if msg["type"] == "LOGIN_SUCCESS":
                    print("Login successfully")
                    join(username)
                if msg["type"] == "LOGIN_FAIL":
                    print("Login failed")
                    disconnect()
                    break
                if msg["type"] == "CHAT":
                    print(f"{msg['sender']}: {msg['content']}")
                if msg["type"] == "PRIVATE":
                    if(msg['receiver'] == username):
                        print(f"[PRIVATE]{msg['sender']}: {msg['content']}")
                    else:
                        pass

            except json.JSONDecodeError:
                print("[SERVER RAW]", text)

        except:
            print("[ERROR] Connection lost")
            break

def disconnect():
    try:
        client.shutdown(socket.SHUT_RDWR) 
    except OSError:
        pass  
    finally:
        client.close()  
    

def send_message(username,msg):
    chat(username,msg)

def connect(host,port):
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("[CONNECTED]")

connect(SERVER_IP,PORT)
username = input("You name: ")
login(username)

threading.Thread(target=recieve_loop, daemon=True).start()

while True:
    msg = input("YOU: ")
    if msg.lower() == "q":
        leave(username)
        disconnect()
        break
    send_message(username,msg)
