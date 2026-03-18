# Giải thích Chat Client (Python Socket)
## 1. Import thư viện

```python
import socket
import threading
import json
import datetime
```

- `socket`: tạo kết nối TCP tới server  
- `threading`: chạy song song (vừa gửi vừa nhận)  
- `json`: encode/decode dữ liệu dạng JSON  
- `datetime`: tạo timestamp cho message  

---

## 2. Biến toàn cục

```python
SERVER_IP=''
PORT=8000

client = None
username = None
```

- `SERVER_IP`, `PORT`: địa chỉ server  
- `client`: socket client  
- `username`: tên người dùng  

---

## 3. Các hàm gửi message

### LOGIN

```python
def login(username):
```

- Tạo message:
```json
{
  "type": "LOGIN",
  "username": "...",
  "timestamp": "..."
}
```

- Chuyển `dict → JSON → bytes`
- Gửi bằng `client.send()`

---

### JOIN

```python
def join(username):
```

- Gửi thông báo user đã vào chat
- Server dùng để quản lý user online

---

### CHAT (public)

```python
def chat(username, content):
```

- Gửi tin nhắn cho tất cả mọi người
- Gồm:
  - `sender`
  - `content`

---

### PRIVATE

```python
def private(sender, receiver, content):
```

- Gửi tin nhắn riêng
- Có thêm `receiver` để server định tuyến đến người muốn gửi

---

### LEAVE

```python
def leave(username):
```

- Thông báo user rời hệ thống

---

## 4. Nhận dữ liệu từ server (recieve_loop)

```python
def recieve_loop():
```

### Luồng chính:
- Chạy vòng lặp vô hạn để luôn lắng nghe server

```python
data = client.recv(1024)
```

- Nhận tối đa 1024 bytes

---

### Nếu server đóng kết nối

```python
if not data:
```

→ In thông báo và thoát

---

### Decode và parse JSON

```python
text = data.decode("utf-8")
msg = json.loads(text)
```

- bytes → string  
- string → dict  

---

### Xử lý từng loại message

#### LOGIN_SUCCESS
```python
if msg["type"] == "LOGIN_SUCCESS":
```
- In thông báo
- Gửi tiếp `JOIN`

---

#### LOGIN_FAIL
```python
if msg["type"] == "LOGIN_FAIL":
```
- Đóng kết nối
- Thoát chương trình

---

#### CHAT
```python
if msg["type"] == "CHAT":
```
- In tin nhắn public:
```
sender: content
```

---

#### PRIVATE
```python
if msg["type"] == "PRIVATE":
```

- Nếu mình là người nhận → hiển thị
```
[PRIVATE]sender: content
```

- Nếu không → bỏ qua

---

### Lỗi JSON

```python
except json.JSONDecodeError:
```

- Nếu server gửi data không phải JSON → in raw

---

### Lỗi kết nối

```python
except:
```

- Khi mất kết nối → thoát loop

---

## 5. Đóng kết nối

```python
def disconnect():
```

- `shutdown()`: tắt gửi và nhận  
- `close()`: đóng socket hoàn toàn  

---

## 6. Gửi tin nhắn

```python
def send_message(username,msg):
```

- Chỉ gọi lại hàm `chat`

---

## 7. Kết nối server

```python
def connect(host,port):
```

- Tạo socket TCP:
```python
socket.AF_INET
socket.SOCK_STREAM
```

- Kết nối tới server

---

## 8. Luồng chính (Main)

### Kết nối & login

```python
connect(SERVER_IP,PORT)
username = input("You name: ")
login(username)
```

---

### Tạo thread nhận dữ liệu

```python
threading.Thread(target=recieve_loop, daemon=True).start()
```

- Chạy song song với luồng chính  
- `daemon=True`: tự tắt khi chương trình kết thúc  

---

### Vòng lặp gửi tin nhắn

```python
while True:
    msg = input("YOU: ")
```

---

### Thoát chương trình

```python
if msg.lower() == "q":
```

- Gửi `LEAVE`
- Đóng kết nối
- Thoát chương trình

---

### Gửi tin nhắn

```python
send_message(username,msg)
```

---

## 9. Tổng kết luồng hoạt động

1. Client kết nối server  
2. User nhập username  
3. Gửi LOGIN  
4. Server phản hồi:
   - OK → JOIN  
   - Fail → disconnect  
5. Client luôn:
   - 1 thread nhận dữ liệu  
   - 1 thread gửi dữ liệu  
6. User chat bình thường  
7. Nhập `q` → thoát  

---
