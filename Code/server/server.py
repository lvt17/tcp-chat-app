import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import protocol

HOST = '0.0.0.0'
PORT = 8000

# {addr: {"socket": conn, "username": str}}
clients = {}
clients_lock = threading.Lock()


def broadcast(msg, exclude_addr=None):
    """Gửi message tới tất cả client, trừ exclude_addr."""
    with clients_lock:
        for addr, client in clients.items():
            if addr != exclude_addr:
                try:
                    protocol.send_message(client["socket"], msg)
                except Exception as e:
                    print(f"[ERROR] Broadcast to {addr}: {e}")


def start_server():
    """Khởi tạo server TCP và bắt đầu lắng nghe kết nối."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[CONNECT] {addr} connected")
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


def handle_client(conn, addr):
    """Xử lý kết nối từ một client: nhận message, route theo type."""
    username = None

    try:
        while True:
            msg = protocol.recv_message(conn)
            if msg is None:
                break

            msg_type = msg.get("type")
            print(f"[{addr}] {msg_type}: {msg}")

            if msg_type == protocol.LOGIN:
                username = msg.get("username")
                # TODO: check trùng username
                with clients_lock:
                    clients[addr] = {"socket": conn, "username": username}
                protocol.send_message(conn, protocol.login_success(username))
                print(f"[LOGIN] {username} logged in")

            elif msg_type == protocol.CHAT:
                broadcast(msg, exclude_addr=addr)

            elif msg_type == protocol.PRIVATE:
                print(f"[PRIVATE] {msg.get('sender')} -> {msg.get('receiver')}: {msg.get('content')}")
                # TODO: gửi riêng cho receiver

            elif msg_type == protocol.LEAVE:
                print(f"[LEAVE] {msg.get('username')}")
                break

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        with clients_lock:
            clients.pop(addr, None)
        conn.close()
        if username:
            print(f"[DISCONNECT] {username} ({addr})")
        else:
            print(f"[DISCONNECT] {addr}")


if __name__ == "__main__":
    start_server()