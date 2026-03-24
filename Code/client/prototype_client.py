import socket
import threading
import json
import queue
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import protocol

SERVER_IP='0.0.0.0'
PORT=8000
"""
!!! watching the explanation in DOCX/research/prototype_explain !!!
"""
 
msg_queue = queue.Queue() # dùng làm queue để tương tác gui


def recieve_loop(client,username):
   while True:
        try:
            msg = protocol.recv_message(client)
            if msg is None:
                print("không nhận được dữ liệu hoặc lỗi")
                disconnect(client, username)
                break

            if msg["type"] == "LOGIN_SUCCESS":
                protocol.send_message(client, protocol.join(username))

            elif msg["type"] == "LOGIN_FAIL":
                msg_queue.put(protocol.error_msg(msg["type"]))
                disconnect(client, username)
                break

            elif msg["type"] == "NOTICE":
                msg_queue.put(msg)

            elif msg["type"] == "CHAT":
                print(msg["content"])
                msg_queue.put(msg)

            elif msg["type"] == "PRIVATE":
                if msg['receiver'] == username:
                   msg_queue.put(msg)
        
        except json.JSONDecodeError as e:
            raw_data = getattr(e, "doc", None)
            msg_queue.put(protocol.error_msg(
                f"[SERVER RAW] lỗi biên dịch JSON, dữ liệu: {raw_data}"
            ))
            # không break, chỉ bỏ qua message lỗi và tiếp tục vòng lặp
            continue

        except Exception as e:
            msg_queue.put(protocol.error_msg(f"Lỗi không xác định: {e}"))
            disconnect(client, username)   # đóng socket luôn
            return  # kết thúc thread



def disconnect(client,username):
    try:
        protocol.send_message(client, protocol.leave(username))
        client.shutdown(socket.SHUT_RDWR) 
    except OSError as e:
        print(f"Error: {e}")
        pass  
    finally:
        client.close()
    

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
protocol.send_message(client,protocol.login(username))

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
            protocol.send_message(client,protocol.private_msg(username,receiver,content))
            print(f"YOU -> {receiver}: {content}")
        else:
            print("Sai cú pháp, vui lòng nhập lại")
            continue
    else:    
        protocol.send_message(client,protocol.chat(username,msg))
        print(f"YOU: {msg}")
