import json
import struct
from datetime import datetime


# message types
LOGIN = "LOGIN"
LOGIN_SUCCESS = "LOGIN_SUCCESS"
LOGIN_FAIL = "LOGIN_FAIL"

CHAT = "CHAT"
PRIVATE = "PRIVATE"

JOIN = "JOIN"
LEAVE = "LEAVE"

USER_LIST = "USER_LIST"

SYSTEM = "SYSTEM"
ERROR = "ERROR"


# get current time
def get_time():
    return datetime.utcnow().isoformat()


# convert dict -> json
def encode_message(msg):
    return json.dumps(msg)


# convert json -> dict
def decode_message(data):
    try:
        return json.loads(data)
    except:
        return None


# login 

def login(username):
    return {
        "type": LOGIN,
        "username": username,
        "timestamp": get_time()
    }


def login_success(username):
    return {
        "type": LOGIN_SUCCESS,
        "username": username,
        "message": "Login successful",
        "timestamp": get_time()
    }


def login_fail(username,reason):
    return {
        "type": LOGIN_FAIL,
        "username": username,
        "reason": reason,
        "timestamp": get_time()
    }


# chat 

def chat(sender, content):
    return {
        "type": CHAT,
        "sender": sender,
        "content": content,
        "timestamp": get_time()
    }


# private message 

def private_msg(sender, receiver, content):
    return {
        "type": PRIVATE,
        "sender": sender,
        "receiver": receiver,
        "content": content,
        "timestamp": get_time()
    }


# join / leave 

def join(username):
    return {
        "type": JOIN,
        "username": username,
        "timestamp": get_time()
    }


def leave(username):
    return {
        "type": LEAVE,
        "username": username,
        "timestamp": get_time()
    }


# user list 

def user_list(users):
    return {
        "type": USER_LIST,
        "users": users,
        "timestamp": get_time()
    }


# system 

def system_msg(text):
    return {
        "type": SYSTEM,
        "content": text,
        "timestamp": get_time()
    }


# error 

def error_msg(text):
    return {
        "type": ERROR,
        "message": text,
        "timestamp": get_time()
    }


# send message to socket
def send_message(sock, msg_dict):
    try:
        data = encode_message(msg_dict).encode("utf-8")
        length = struct.pack("!I", len(data))
        sock.sendall(length + data)
    except Exception as e:
        print("Send error:", e)
        sock.close()


# receive message from socket
def recv_message(sock):
    try:
        raw_length = recvall(sock, 4)
        if not raw_length:
            return None

        length = struct.unpack("!I", raw_length)[0]
        data = recvall(sock, length)
        if not data:
            return None

        msg = decode_message(data.decode("utf-8"))

        if msg is None:
            return error_msg("Invalid JSON")
        
        valid, err = validate_message(msg)
        if not valid:
            return error_msg(err)
        
        return msg
    

    except Exception as e:
        print("Receive error:", e)
        return None


# helper: read n bytes
def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


# validation 

REQUIRED_FIELDS = {
    LOGIN: ["type", "username", "timestamp"],
    CHAT: ["type", "sender", "content", "timestamp"],
    PRIVATE: ["type", "sender", "receiver", "content", "timestamp"],
    JOIN: ["type", "username", "timestamp"],
    LEAVE: ["type", "username", "timestamp"],
    USER_LIST: ["type", "users", "timestamp"],
}

def validate_message(msg):
    if not isinstance(msg, dict):
        return False, "Message không hợp lệ"

    msg_type = msg.get("type")
    if msg_type not in REQUIRED_FIELDS:
        return False, "Unknown type"

    for field in REQUIRED_FIELDS[msg_type]:
        if field not in msg or msg[field] is None:
            return False, f"Thiếu field: {field}"

    if "content" in msg:
        if not msg["content"].strip():
            return False, "Content rỗng"
        if len(msg["content"]) > 1000:
            return False, "Content quá dài"

    return True, None