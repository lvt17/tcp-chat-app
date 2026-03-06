# Protocol Specification

## 1. Message Types

Trong hệ thống **Chat Application via TCP**, client và server giao tiếp với nhau thông qua các message được định dạng dưới dạng **JSON**.  
Mỗi message đều chứa trường `type` để xác định loại message và cách hệ thống xử lý.

Hệ thống sử dụng các loại message chính: **CHAT, JOIN, LEAVE, PRIVATE, SYSTEM**.

### 1.1 CHAT

Message **CHAT** được sử dụng khi người dùng gửi tin nhắn trong phòng chat.  
Server sẽ nhận message này và **broadcast** tin nhắn đến tất cả các client đang kết nối.

**Fields:**
- `sender`: tên người gửi
- `content`: nội dung tin nhắn
- `timestamp`: thời gian gửi tin nhắn

### 1.2 JOIN

Message **JOIN** được gửi khi người dùng kết nối và tham gia phòng chat.  
Server sẽ thêm người dùng vào danh sách các client đang online.

**Fields:**
- `username`: tên người dùng
- `timestamp`: thời điểm tham gia

### 1.3 LEAVE

Message **LEAVE** được gửi khi người dùng rời khỏi phòng chat hoặc ngắt kết nối khỏi server.  
Server sẽ xóa người dùng khỏi danh sách các client đang online.

**Fields:**
- `username`: tên người dùng rời phòng
- `timestamp`: thời điểm rời khỏi hệ thống

### 1.4 PRIVATE

Message **PRIVATE** được sử dụng để gửi tin nhắn riêng giữa hai người dùng.  
Tin nhắn này chỉ được gửi đến người nhận cụ thể và **không broadcast** cho toàn bộ phòng chat.

**Fields:**
- `sender`: người gửi
- `receiver`: người nhận
- `content`: nội dung tin nhắn
- `timestamp`: thời gian gửi

### 1.5 SYSTEM (Optional)

Message **SYSTEM** được tạo bởi server để gửi các thông báo hệ thống, ví dụ khi người dùng tham gia hoặc rời phòng chat.

**Fields:**
- `content`: nội dung thông báo
- `timestamp`: thời gian thông báo

---

## 2. JSON Format

Tất cả message được gửi dưới dạng **JSON**.

### CHAT message
```json
{
  "type": "CHAT",
  "sender": "user1",
  "content": "Hello!",
  "timestamp": "2025-03-06T20:00:00"
}
```

### JOIN message
```json
{
  "type": "JOIN",
  "username": "user1",
  "timestamp": "2025-03-06T20:00:00"
}
```

### LEAVE message
```json
{
  "type": "LEAVE",
  "username": "user1",
  "timestamp": "2025-03-06T20:00:00"
}
```

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

### SYSTEM message
```json
{
  "type": "SYSTEM",
  "content": "user1 joined the chat",
  "timestamp": "2025-03-06T20:00:00"
}
```
