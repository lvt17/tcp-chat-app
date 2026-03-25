import socket
import struct
import queue
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import protocol

SERVER_IP = '127.0.0.1'
PORT = 8000

msg_queue = queue.Queue()



def recieve_loop(client, username):   
    while True:
        try:
            msg = protocol.recv_message(client)

            if msg is None:
                print("[DISCONNECT] Server closed")
                disconnect(client, username)
                break

            msg_type = msg.get("type")

            # ===== LOGIN =====
            if msg_type == protocol.LOGIN_SUCCESS:
                send_message(client, protocol.join(username))

            elif msg_type == protocol.LOGIN_FAIL:
                msg_queue.put({
                    "type": "SYSTEM",
                    "content": msg.get("reason")
                })
                disconnect(client, username)
                break

            # ===== CHAT =====
            elif msg_type == protocol.CHAT:
                msg_queue.put(msg)

            # ===== PRIVATE =====
            elif msg_type == protocol.PRIVATE:
                if msg.get("receiver") == username or msg.get("sender") == username:
                    msg_queue.put(msg)

            # ===== SYSTEM =====
            elif msg_type == protocol.SYSTEM:
                msg_queue.put(msg)

            # ===== USER LIST =====
            elif msg_type == protocol.USER_LIST:
                msg_queue.put(msg)

            # ===== ERROR =====
            elif msg_type == protocol.ERROR:
                msg_queue.put({
                    "type": "SYSTEM",
                    "content": msg.get("message")
                })

        except Exception as e:
            msg_queue.put({
                "type": "SYSTEM",
                "content": f"Lỗi: {e}"
            })
            break


def send_message(client, msg):
    protocol.send_message(client, msg)   



def connect_to_server(host, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print("[CONNECTED]")
        return client
    except Exception as e:
        print(f"Error occured: {e}")
        return None


def disconnect(client, username):
    try:
        send_message(client, protocol.leave(username))
        client.shutdown(socket.SHUT_RDWR)
    except:
        pass
    finally:
        client.close()


def private(sender, receiver, content):
    return protocol.private_msg(sender, receiver, content)

def chat(sender, content):
    return protocol.chat(sender, content)

def login(username):
    return protocol.login(username)

def join(username):
    return protocol.join(username)

def leave(username):
    return protocol.leave(username)