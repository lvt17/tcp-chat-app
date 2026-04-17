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
    """Tim server tren LAN qua UDP broadcast/passive + active probe.

    Tra ve (ip, port) hoac None.
    """
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.settimeout(0.5)

    listening_mode = True
    try:
        # Passive mode: nhan broadcast dinh ky tu server.
        udp_sock.bind(("", DISCOVER_PORT))
    except OSError:
        # Port da duoc dung (vd server/client cung may), fallback active mode.
        listening_mode = False
        udp_sock.bind(("", 0))

    # Chu dong yeu cau server tra loi de tang ti le tim thay tren mot so mang Wi-Fi.
    try:
        udp_sock.sendto(b"DISCOVER_CHAT_SERVER", ("255.255.255.255", DISCOVER_PORT))
    except Exception:
        pass

    import time
    deadline = time.time() + max(timeout, 0.5)

    try:
        while time.time() < deadline:
            try:
                data, addr = udp_sock.recvfrom(1024)
            except socket.timeout:
                continue

            msg = data.decode("utf-8", errors="ignore")
            if msg.startswith("CHAT_SERVER:"):
                try:
                    port = int(msg.split(":", 1)[1])
                    return (addr[0], port)
                except ValueError:
                    continue

            # Nếu đang passive mode, hết 0.5s timeout vẫn tiếp tục nghe đến deadline.
            if listening_mode:
                continue
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

    # thread in tin nhan tu queue ra man hinh terminal
    def print_loop():
        while True:
            try:
                msg = msg_queue.get()
                m_type = msg.get("type")
                if m_type == "SYSTEM":
                    print(f"\n[SYSTEM] {msg.get('content')}")
                elif m_type == protocol.CHAT:
                    print(f"\n[{msg.get('sender')}] {msg.get('content')}")
                elif m_type == protocol.PRIVATE:
                    print(f"\n[PM tu {msg.get('sender')}] {msg.get('content')}")
                elif m_type == protocol.USER_LIST:
                    print(f"\n[USERS] {', '.join(msg.get('users'))}")
            except:
                break

    threading.Thread(target=print_loop, daemon=True).start()

    print("Commands: /pm <user> <msg> = private | q = quit")
    while True:
        try:
            msg = input("> ") # them prompt de biet dang cho nhap
            if not msg: continue
            if msg.lower() == "q":
                disconnect(client, username)
                break
            elif msg.startswith("/pm "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    send_message(client, private(username, parts[1], parts[2]))
                else:
                    print("Usage: /pm <username> <message>")
            else:
                send_message(client, chat(username, msg))
        except EOFError:
            break
        except Exception as e:
            print(f"Lỗi nhập liệu: {e}")
            break