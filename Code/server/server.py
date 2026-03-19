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


def send_private(msg, receiver_username, sender_conn):
    """Gửi tin nhắn riêng tới một user. Báo lỗi nếu user không online."""
    with clients_lock:
        for addr, client in clients.items():
            if client["username"] == receiver_username:
                try:
                    protocol.send_message(client["socket"], msg)
                    return True
                except Exception as e:
                    print(f"[ERROR] Private to {receiver_username}: {e}")
                    return False

    # User không tìm thấy
    protocol.send_message(sender_conn, protocol.error_msg(f"User '{receiver_username}' không online"))
    return False


def is_username_taken(username):
    """Kiểm tra username đã được sử dụng chưa."""
    with clients_lock:
        return any(c["username"] == username for c in clients.values())


def get_online_usernames():
    """Lấy danh sách username đang online."""
    with clients_lock:
        return [c["username"] for c in clients.values()]


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

                if is_username_taken(username):
                    protocol.send_message(conn, protocol.login_fail(username, "Username đã được sử dụng"))
                    username = None
                    continue

                with clients_lock:
                    clients[addr] = {"socket": conn, "username": username}

                protocol.send_message(conn, protocol.login_success(username))
                print(f"[LOGIN] {username} logged in")

            elif msg_type == protocol.JOIN:
                # Thông báo cho tất cả user khác
                broadcast(protocol.system_msg(f"{username} đã tham gia"), exclude_addr=addr)
                # Gửi danh sách user online cho client mới
                protocol.send_message(conn, protocol.user_list(get_online_usernames()))

            elif msg_type == protocol.CHAT:
                broadcast(msg, exclude_addr=addr)

            elif msg_type == protocol.PRIVATE:
                receiver = msg.get("receiver")
                send_private(msg, receiver, conn)

            elif msg_type == protocol.LEAVE:
                print(f"[LEAVE] {username}")
                break

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        with clients_lock:
            clients.pop(addr, None)
        conn.close()

        if username:
            broadcast(protocol.system_msg(f"{username} đã rời đi"))
            broadcast(protocol.user_list(get_online_usernames()))
            print(f"[DISCONNECT] {username} ({addr})")
        else:
            print(f"[DISCONNECT] {addr}")


if __name__ == "__main__":
    start_server()