# Server Explain (Issue #14) — Luu lich su chat bang SQLite

## Tong quan

Issue #14 bo sung tinh nang luu lich su tin nhan vao SQLite database.
Khi user moi ket noi, server gui lai 50 tin nhan gan nhat de user doc lai lich su chat.

---

## Cau truc file

```
Code/server/
├── server.py      # server chinh, xu ly ket noi
├── database.py    # module quan ly SQLite (NEW)
└── __init__.py
```

Tach `database.py` rieng de:
- Code gon, de bao tri
- De thay doi database engine sau nay (vi du: PostgreSQL)
- Server.py chi can goi ham, khong can biet chi tiet SQL

---

## database.py

### Bang messages

```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    receiver TEXT DEFAULT NULL
)
```

- `receiver = NULL` → tin nhan public (broadcast)
- `receiver = "username"` → tin nhan private

### Cac ham chinh

#### init_db()
Tao bang `messages` neu chua ton tai. Goi 1 lan khi server khoi dong.

#### save_message(sender, content, timestamp, receiver=None)
Luu 1 tin nhan vao database.
- `receiver=None` → tin public
- `receiver="bob"` → tin private gui cho bob

#### get_recent_messages(limit=50)
Lay N tin nhan public gan nhat (khong lay tin private de bao mat).

```python
# chi lay tin public (receiver IS NULL)
cursor.execute(
    "SELECT sender, content, timestamp, receiver FROM messages "
    "WHERE receiver IS NULL "
    "ORDER BY id DESC LIMIT ?",
    (limit,)
)
```

Ket qua duoc dao nguoc (`reverse()`) de tin cu hien truoc, tin moi hien sau.

### Thread Safety

```python
db_lock = threading.Lock()

def save_message(...):
    with db_lock:          # chi 1 thread duoc ghi tai 1 thoi diem
        conn = sqlite3.connect(DB_PATH)
        ...
        conn.close()
```

SQLite khong ho tro tot nhieu thread ghi dong thoi, nen can `Lock` de dam bao an toan.
Moi ham tu mo va dong connection rieng, tranh van de shared connection giua cac thread.

---

## Tich hop vao server.py

### 1. Khoi tao database khi server start

```python
def start_server():
    database.init_db()
    print("[SERVER] Database initialized")
    ...
```

### 2. Luu tin nhan khi nhan CHAT

```python
elif msg_type == protocol.CHAT:
    database.save_message(
        sender=msg.get("sender"),
        content=msg.get("content"),
        timestamp=msg.get("timestamp")
    )
    broadcast(msg, exclude_addr=addr)
```

Luu truoc, broadcast sau. Neu broadcast loi thi tin nhan van duoc luu.

### 3. Luu tin nhan PRIVATE

```python
elif msg_type == protocol.PRIVATE:
    receiver = msg.get("receiver")
    database.save_message(
        sender=msg.get("sender"),
        content=msg.get("content"),
        timestamp=msg.get("timestamp"),
        receiver=receiver          # khac NULL → tin private
    )
    send_private(msg, receiver, conn)
```

### 4. Gui lich su chat khi user JOIN

```python
elif msg_type == protocol.JOIN:
    broadcast(...)
    protocol.send_message(conn, protocol.user_list(get_online_usernames()))

    # gui lich su chat
    history = database.get_recent_messages(50)
    for h in history:
        protocol.send_message(conn, protocol.chat(h["sender"], h["content"]))
```

Server gui tung tin nhan cu duoi dang CHAT message.
Client nhan va hien thi giong tin nhan binh thuong.

---

## Flow tong the

```
Server start
    |
    v
init_db() → tao bang messages
    |
    v
Client A connect → LOGIN → JOIN
    |
    v
Server gui USER_LIST + 50 tin nhan cu
    |
    v
Client A gui "Hello" (CHAT)
    |
    v
Server: save_message() → broadcast()
    |
    v
Client B nhan "Hello"
    |
    v
Client B gui "/private A secret" (PRIVATE)
    |
    v
Server: save_message(receiver="A") → send_private()
    |
    v
Chi Client A nhan "secret"
```

---

## Luu y

1. **Chi gui lich su public**: Tin private khong gui lai cho user khac (bao mat)
2. **File database**: `chat_history.db` tao tai thu muc chay server
3. **Hieu nang**: Voi 50 tin nhan, khong anh huong hieu nang. Neu can nhieu hon, can them phan trang (pagination)
