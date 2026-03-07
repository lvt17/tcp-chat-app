# Protocol Specification

## 1. Message Types

Trong hệ thống **Chat Application via TCP**, client và server giao tiếp với nhau thông qua các message được định dạng dưới dạng **JSON**.  
Mỗi message đều chứa trường `type` để xác định loại message và cách hệ thống xử lý.

Hệ thống sử dụng các loại message chính:  
**LOGIN, LOGIN_SUCCESS, LOGIN_FAIL, CHAT, JOIN, LEAVE, PRIVATE, USER_LIST, SYSTEM, ERROR**

---

### LOGIN

Message **LOGIN** được gửi từ client đến server khi người dùng muốn đăng nhập vào hệ thống.

Server sẽ kiểm tra xem **username đã tồn tại hoặc đang được sử dụng hay chưa**.

**Fields:**

- `username`: tên người dùng  
- `timestamp`: thời gian gửi yêu cầu  

---

### LOGIN_SUCCESS

Message **LOGIN_SUCCESS** được gửi từ server đến client khi đăng nhập thành công.

Server sẽ thêm người dùng vào danh sách các client đang online.

**Fields:**

- `username`: tên người dùng  
- `message`: thông báo đăng nhập thành công  
- `timestamp`: thời gian phản hồi  

---

### LOGIN_FAIL

Message **LOGIN_FAIL** được gửi từ server đến client khi đăng nhập thất bại.

**Fields:**

- `username`: tên người dùng  
- `reason`: lý do thất bại  
- `timestamp`: thời gian phản hồi  

---

### CHAT

Message **CHAT** được sử dụng khi người dùng gửi tin nhắn trong phòng chat.  
Server sẽ nhận message này và **broadcast** tin nhắn đến tất cả các client đang kết nối.

**Fields:**

- `sender`: tên người gửi  
- `content`: nội dung tin nhắn  
- `timestamp`: thời gian gửi tin nhắn  

---

### JOIN

Message **JOIN** được gửi khi người dùng kết nối và tham gia phòng chat.  
Server sẽ thêm người dùng vào danh sách các client đang online.

**Fields:**

- `username`: tên người dùng  
- `timestamp`: thời điểm tham gia  

---

### LEAVE

Message **LEAVE** được gửi khi người dùng rời khỏi phòng chat hoặc ngắt kết nối khỏi server.  
Server sẽ xóa người dùng khỏi danh sách các client đang online.

**Fields:**

- `username`: tên người dùng rời phòng  
- `timestamp`: thời điểm rời khỏi hệ thống  

---

### PRIVATE

Message **PRIVATE** được sử dụng để gửi tin nhắn riêng giữa hai người dùng.  
Tin nhắn này chỉ được gửi đến người nhận cụ thể và **không broadcast** cho toàn bộ phòng chat.

**Fields:**

- `sender`: người gửi  
- `receiver`: người nhận  
- `content`: nội dung tin nhắn  
- `timestamp`: thời gian gửi  

---

### USER_LIST

Message **USER_LIST** được gửi từ server đến client để cung cấp danh sách người dùng đang online.

**Fields:**

- `users`: danh sách username  
- `timestamp`: thời gian gửi  

---

### SYSTEM (Optional)

Message **SYSTEM** được tạo bởi server để gửi các thông báo hệ thống, ví dụ khi người dùng tham gia hoặc rời phòng chat.

**Fields:**

- `content`: nội dung thông báo  
- `timestamp`: thời gian thông báo  

---

## 2. JSON Format

Tất cả message được gửi dưới dạng **JSON**.

### LOGIN message

```json
{
  "type": "LOGIN",
  "username": "user1",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### LOGIN_SUCCESS message

```json
{
  "type": "LOGIN_SUCCESS",
  "username": "user1",
  "message": "Login successful",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### LOGIN_FAIL message

```json
{
  "type": "LOGIN_FAIL",
  "username": "user1",
  "reason": "Username already taken",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### CHAT message

```json
{
  "type": "CHAT",
  "sender": "user1",
  "content": "Hello!",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### JOIN message

```json
{
  "type": "JOIN",
  "username": "user1",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### LEAVE message

```json
{
  "type": "LEAVE",
  "username": "user1",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### PRIVATE message

```json
{
  "type": "PRIVATE",
  "sender": "user1",
  "receiver": "user2",
  "content": "Hello!",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### USER_LIST message

```json
{
  "type": "USER_LIST",
  "users": ["user1", "user2", "user3"],
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### SYSTEM message

```json
{
  "type": "SYSTEM",
  "content": "user1 joined the chat",
  "timestamp": "2025-03-06T20:00:00"
}
```

---

### ERROR message

```json
{
  "type": "ERROR",
  "message": "Invalid message format",
  "timestamp": "2025-03-06T20:00:00"
}
```
