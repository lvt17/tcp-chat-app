import socket
import threading
import signal
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import protocol
sys.path.insert(0, os.path.dirname(__file__))
import database

HOST = '0.0.0.0'
PORT = 8000

clients = {}
clients_lock = threading.Lock()

server_socket = None


def broadcast(msg, exclude_addr=None):
    """Gửi message tới tất cả client."""
    with clients_lock:
        for addr, client in list(clients.items()):
            if exclude_addr and addr == exclude_addr:
                continue
            try:
                protocol.send_message(client["socket"], msg)
            except Exception as e:
                print(f"[ERROR] Broadcast to {addr}: {e}")


def broadcast_user_list():
    """Gửi danh sách user online cho tất cả client."""
    users = get_online_usernames()
    broadcast(protocol.user_list(users))


def send_private(msg, receiver_username, sender_conn):
    """Gửi tin nhắn riêng cho cả sender và receiver"""

    sent = False

    with clients_lock:
        for addr, client in clients.items():

            # gửi cho receiver
            if client["username"] == receiver_username:
                try:
                    protocol.send_message(client["socket"], msg)
                    sent = True
                except Exception as e:
                    print(f"[ERROR] Private to {receiver_username}: {e}")

            # gửi lại cho sender
            if client["socket"] == sender_conn:
                try:
                    protocol.send_message(client["socket"], msg)
                except Exception as e:
                    print(f"[ERROR] Private echo sender: {e}")

    if not sent:
        protocol.send_message(
            sender_conn,
            protocol.error_msg(f"User '{receiver_username}' không online")
        )


def is_username_taken(username):
    with clients_lock:
        return any(c["username"] == username for c in clients.values())


def get_online_usernames():
    with clients_lock:
        return [c["username"] for c in clients.values()]


def remove_client(addr, username):
    with clients_lock:
        client = clients.pop(addr, None)
        if client:
            try:
                client["socket"].close()
            except:
                pass

    if username:
        broadcast(protocol.system_msg(f"{username} đã rời đi"))
        broadcast_user_list()
        print(f"[DISCONNECT] {username} ({addr})")
    else:
        print(f"[DISCONNECT] {addr}")


def handle_client(conn, addr):
    username = None

    try:
        while True:

            msg = protocol.recv_message(conn)

            if msg is None:
                break

            msg_type = msg.get("type")

            print(f"[{addr}] {msg_type}: {msg}")

            # ================= LOGIN =================
            if msg_type == protocol.LOGIN:

                username = msg.get("username")

                if not username or not username.strip():
                    protocol.send_message(
                        conn,
                        protocol.login_fail("", "Username không được để trống")
                    )
                    username = None
                    continue

                if is_username_taken(username):
                    protocol.send_message(
                        conn,
                        protocol.login_fail(username, "Username đã được sử dụng")
                    )
                    username = None
                    continue

                with clients_lock:
                    clients[addr] = {
                        "socket": conn,
                        "username": username
                    }

                protocol.send_message(
                    conn,
                    protocol.login_success(username)
                )

                print(f"[LOGIN] {username} logged in")

                # cập nhật user list cho tất cả
                broadcast_user_list()

            # ================= JOIN =================
            elif msg_type == protocol.JOIN:

                broadcast(
                    protocol.system_msg(f"{username} đã tham gia")
                )

                broadcast_user_list()

                # gửi lịch sử chat cho client mới
                history = database.get_recent_messages(50)

                for h in history:
                    protocol.send_message(
                        conn,
                        protocol.chat(
                            h["sender"],
                            h["content"]
                        )
                    )

            # ================= PUBLIC CHAT =================
            elif msg_type == protocol.CHAT:

                database.save_message(
                    sender=msg.get("sender"),
                    content=msg.get("content"),
                    timestamp=msg.get("timestamp")
                )

                broadcast(msg)

            # ================= PRIVATE CHAT =================
            elif msg_type == protocol.PRIVATE:

                receiver = msg.get("receiver")

                database.save_message(
                    sender=msg.get("sender"),
                    content=msg.get("content"),
                    timestamp=msg.get("timestamp"),
                    receiver=receiver
                )

                send_private(msg, receiver, conn)

            # ================= LEAVE =================
            elif msg_type == protocol.LEAVE:

                print(f"[LEAVE] {username}")
                break

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:
        remove_client(addr, username)


def shutdown_server(sig, frame):
    print("\n[SERVER] Shutting down...")

    broadcast(protocol.system_msg("Server đang tắt..."))

    with clients_lock:
        for addr, client in list(clients.items()):
            try:
                client["socket"].close()
            except:
                pass

        clients.clear()

    if server_socket:
        server_socket.close()

    sys.exit(0)


def start_server():
    global server_socket

    signal.signal(signal.SIGINT, shutdown_server)

    database.init_db()
    print("[SERVER] Database initialized")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))

    server_socket.listen()

    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        try:

            conn, addr = server_socket.accept()

            print(f"[CONNECT] {addr} connected")

            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )

            thread.start()

        except OSError:
            break


if __name__ == "__main__":
    start_server()