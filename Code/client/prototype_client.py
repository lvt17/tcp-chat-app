import socket
import struct
import queue
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import protocol

DEFAULT_PORT = 8000
DISCOVER_PORT = 9999


def discover_server(timeout=3):
    """Lang nghe UDP broadcast de tu tim server tren LAN. Tra ve (ip, port) hoac None."""
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("", DISCOVER_PORT))
    udp_sock.settimeout(timeout)
    try:
        data, addr = udp_sock.recvfrom(1024)
        msg = data.decode("utf-8")
        if msg.startswith("CHAT_SERVER:"):
            port = int(msg.split(":")[1])
            return (addr[0], port)
    except socket.timeout:
        return None
    finally:
        udp_sock.close()

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


# chay truc tiep de test terminal (khong anh huong khi GUI import)
if __name__ == "__main__":
    import threading

    ip = input("Server IP (Enter de tu tim): ").strip()
    port = DEFAULT_PORT

    if not ip:
        print("Dang tim server tren mang LAN...")
        result = discover_server(timeout=3)
        if result:
            ip, port = result
            print(f"Tim thay server: {ip}:{port}")
        else:
            print("Khong tim thay server. Nhap IP thu cong:")
            ip = input("Server IP: ").strip() or "127.0.0.1"

    username = input("Username: ")

    client = connect_to_server(ip, port)
    if not client:
        print("Khong ket noi duoc server")
        sys.exit(1)

    send_message(client, login(username))

    threading.Thread(target=recieve_loop, args=(client, username), daemon=True).start()

    print("Commands: /pm <user> <msg> = private | q = quit")
    while True:
        msg = input()
        if msg.lower() == "q":
            disconnect(client, username)
            break
        elif msg.startswith("/pm "):
            parts = msg.split(" ", 2)
            if len(parts) >= 3:
                send_message(client, private(username, parts[1], parts[2]))
                print(f"[-> {parts[1]}] {parts[2]}")
            else:
                print("Usage: /pm <username> <message>")
        else:
            send_message(client, chat(username, msg))