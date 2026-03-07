import json
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
    return json.loads(data)


# -------- login --------

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
        "timestamp": get_time()
    }


def login_fail(reason):
    return {
        "type": LOGIN_FAIL,
        "reason": reason,
        "timestamp": get_time()
    }


# -------- chat --------

def chat(sender, content):
    return {
        "type": CHAT,
        "sender": sender,
        "content": content,
        "timestamp": get_time()
    }


# -------- private message --------

def private_msg(sender, receiver, content):
    return {
        "type": PRIVATE,
        "sender": sender,
        "receiver": receiver,
        "content": content,
        "timestamp": get_time()
    }


# -------- join / leave --------

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


# -------- user list --------

def user_list(users):
    return {
        "type": USER_LIST,
        "users": users,
        "timestamp": get_time()
    }


# -------- system --------

def system_msg(text):
    return {
        "type": SYSTEM,
        "content": text,
        "timestamp": get_time()
    }


# -------- error --------

def error_msg(text):
    return {
        "type": ERROR,
        "message": text,
        "timestamp": get_time()
    }