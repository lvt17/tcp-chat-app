import socket
import threading
import json
import datetime
import struct
import queue
SERVER_IP='0.0.0.0'
PORT=8000
"""
!!! watching the explanation in DOCX/research/prototype_explain !!!
"""

msg_queue = queue.Queue() # dùng làm queue để tương tác gui

def login(username):
    msg = {
        "type": "LOGIN",
        "username": username,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return msg

def join(username):
    msg = {
        "type": "JOIN",
        "username": username,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return msg

def chat(username, content):
    msg = {
        "type": "CHAT",
        "sender": username,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return msg

def private(sender, receiver, content):
    msg = {
        "type": "PRIVATE",
        "sender": sender,
        "receiver": receiver,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return msg

def leave(username):
    msg = {
        "type": "LEAVE",
        "username": username,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return msg

def error_msg(error):
    msg = {
        "type": "ERROR",
        "content": error,
        "timestamp": datetime.datetime.now().isoformat()
    }
    return msg


def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def encode_message(msg):
    return json.dumps(msg)

def decode_message(data):
    return json.loads(data)

def recieve_loop(client,username):
    while True:
        try:
            raw_length = recvall(client,4)
            if not raw_length:
                print("[DISCONNECT] Server closed connection")
                disconnect(client,username)
                break
            try:
                length = struct.unpack("!I", raw_length)[0]
                data = recvall(client, length)
                msg = decode_message(data.decode("utf-8")) 
                if msg["type"] == "LOGIN_SUCCESS":
                    send_message(client,join(username)) 
                if msg["type"] == "LOGIN_FAIL":
                    msg_queue.put(error_msg(msg["type"])) # khi nhận message thì gửi vào queue gui sẽ lấy message để cập nhật gui
                    disconnect(client,username)
                    break
                if msg["type"] == "NOTICE":
                   msg_queue.put(msg)
                if msg["type"] == "CHAT":
                   msg_queue.put(msg)
                if msg["type"] == "PRIVATE":
                    if(msg['receiver'] == username):
                        msg_queue.put(msg)
                    else:
                        pass

            except json.JSONDecodeError:
                msg_queue.put(error_msg(f"[SERVER RAW] lỗi biên dịch json show json raw: {data.decode('utf-8')}"))
        except Exception as e:
            msg_queue.put(error_msg(f"[ERROR] Connection lost: {e}"))
            break

def disconnect(client,username):
    try:
        send_message(client,leave(username))
        client.shutdown(socket.SHUT_RDWR) 
    except OSError as e:
        print(f"Error: {e}")
        pass  
    finally:
        client.close()
    

def send_message(client,dict): # done
    try:
        data = encode_message(dict).encode("utf-8")
        length = struct.pack("!I", len(data))
        client.sendall(length + data)
    except OSError as e:
        print(f"[ERROR] Failed to send message: {e}")
    except Exception as e:
         print(f"[ERROR] Unexpected error: {e}")


def connect_to_server(host,port): # done
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print("[CONNECTED]")
        return client
    except Exception as e:
        print(f"Error occured:{e}")
        return None
    

client = connect_to_server(SERVER_IP,PORT)
username = input("You name: ")
send_message(client,login(username))
threading.Thread(target=recieve_loop,args = (client,username), daemon=True).start()

while True:
    msg = input()
    if msg.lower() == "q":
        disconnect(client,username)
        break
    elif msg.lower().startswith("/private"):
        parts = msg.split(" ", 2)
        
        if len(parts) >= 3:
            receiver = parts[1]
            content = parts[2]
            send_message(client,private(username,receiver,content))
            print(f"YOU -> {receiver}: {content}")
        else:
            print("Sai cú pháp, vui lòng nhập lại")
            continue
    else:    
        send_message(client,chat(username,msg))
        print(f"YOU: {msg}")
