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
    """Xử lý kết nối từ một client."""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode("utf-8")
            print(f"[{addr}] {msg}")

            reply = f"Server received: {msg}"
            conn.send(reply.encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()
        print(f"[DISCONNECT] {addr}")


if __name__ == "__main__":
    start_server()