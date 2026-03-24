# Protocol Specification

## 1. Message Types

Trong hệ thống **Chat Application via TCP**, client và server giao tiếp với nhau thông qua các message được định dạng dưới dạng **JSON**.  
Mỗi message đều chứa trường `type` để xác định loại message và cách hệ thống xử lý.

Hệ thống sử dụng các loại message chính:  
**LOGIN, LOGIN_SUCCESS, LOGIN_FAIL, CHAT, JOIN, LEAVE, PRIVATE, USER_LIST, SYSTEM, ERROR**


### LOGIN

Message **LOGIN** được gửi từ client đến server khi người dùng muốn đăng nhập vào hệ thống.

Server sẽ kiểm tra xem **username đã tồn tại hoặc đang được sử dụng hay chưa**.

**Fields:**
- `type`: LOGIN
- `username`: tên người dùng  
- `timestamp`: thời gian gửi yêu cầu  


### LOGIN_SUCCESS

Message **LOGIN_SUCCESS** được gửi từ server đến client khi đăng nhập thành công.

Server xác nhận username hợp lệ.  
Sau khi nhận **LOGIN_SUCCESS**, client cần gửi **JOIN** để tham gia phòng chat.

**Fields:**

- `type`: LOGIN_SUCCESS
- `username`: tên người dùng  
- `message`: thông báo đăng nhập thành công  
- `timestamp`: thời gian phản hồi


### LOGIN_FAIL

Message **LOGIN_FAIL** được gửi từ server đến client khi đăng nhập thất bại.

**Fields:**

- `type`: LOGIN_FAIL
- `username`: tên người dùng  
- `reason`: lý do thất bại  
- `timestamp`: thời gian phản hồi  


### CHAT

Message **CHAT** được sử dụng khi người dùng gửi tin nhắn trong phòng chat.  
Server sẽ nhận message này và broadcast tin nhắn đến tất cả các client đang kết nối.

**Fields:**

- `type`: CHAT
- `sender`: tên người gửi (username)  
- `content`: nội dung tin nhắn  
- `timestamp`: thời gian gửi tin nhắn  


### JOIN

Message **JOIN** được gửi từ client đến server sau khi đăng nhập thành công
để tham gia phòng chat.

Khi server nhận được message này, server sẽ:
- Thêm người dùng vào danh sách các client đang online
- Gửi thông báo SYSTEM cho các client khác
- Cập nhật USER_LIST cho các client

**Fields:**

- `type`: JOIN
- `username`: tên người dùng  
- `timestamp`: thời điểm tham gia


### LEAVE

Message **LEAVE** được gửi khi người dùng rời khỏi phòng chat hoặc ngắt kết nối khỏi server.  
Server sẽ xóa người dùng khỏi danh sách các client đang online.

**Fields:**

- `type`: LEAVE
- `username`: tên người dùng rời phòng  
- `timestamp`: thời điểm rời khỏi hệ thống  


### PRIVATE

Message **PRIVATE** được sử dụng để gửi tin nhắn riêng giữa hai người dùng.  
Tin nhắn này chỉ được gửi đến người nhận cụ thể và **không broadcast** cho toàn bộ phòng chat.

**Fields:**

- `type`: PRIVATE
- `sender`: tên người gửi (username)
- `receiver`: tên người nhận (username)  
- `content`: nội dung tin nhắn  
- `timestamp`: thời gian gửi  


### USER_LIST

Message **USER_LIST** được gửi từ server đến client để cung cấp danh sách người dùng đang online.

**Fields:**

- `type`: USER_LIST
- `users`: danh sách username  
- `timestamp`: thời gian gửi  


### SYSTEM (Optional)

Message **SYSTEM** được tạo bởi server để gửi các thông báo hệ thống, ví dụ khi người dùng tham gia hoặc rời phòng chat.

**Fields:**

- `type`: SYSTEM
- `content`: nội dung thông báo  
- `timestamp`: thời gian thông báo  


### ERROR

Message **ERROR** được gửi khi xảy ra lỗi trong quá trình xử lý message.

**Fields:**

- `type`: ERROR
- `message`: nội dung lỗi
- `timestamp`: thời gian xảy ra lỗi


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


### LOGIN_SUCCESS message

```json
{
  "type": "LOGIN_SUCCESS",
  "username": "user1",
  "message": "Login successful",
  "timestamp": "2025-03-06T20:00:00"
}
```


### LOGIN_FAIL message

```json
{
  "type": "LOGIN_FAIL",
  "username": "user1",
  "reason": "Username already taken",
  "timestamp": "2025-03-06T20:00:00"
}
```


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


### USER_LIST message

```json
{
  "type": "USER_LIST",
  "users": ["user1", "user2", "user3"],
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


### ERROR message

```json
{
  "type": "ERROR",
  "message": "Invalid message format",
  "timestamp": "2025-03-06T20:00:00"
}
```
## 3. Các hàm hỗ trợ (Utility Functions)

Trong file protocol.py, hệ thống sử dụng một số hàm hỗ trợ để tạo và xử lý message.
Các hàm này giúp dữ liệu giữa client và server luôn thống nhất về định dạng.

get_time(): tạo thời gian hiện tại theo chuẩn UTC để gắn vào trường timestamp
encode_message(msg): chuyển message từ kiểu dict sang chuỗi JSON trước khi gửi
decode_message(data): chuyển chuỗi JSON nhận được thành dict để chương trình xử lý

Nhờ các hàm này, mọi message trong hệ thống đều có cấu trúc rõ ràng, dễ kiểm tra và dễ mở rộng.

## 4. Truyền và nhận message

Vì hệ thống sử dụng TCP, dữ liệu được truyền dưới dạng một luồng byte liên tục.
Nếu chỉ gửi JSON trực tiếp, có thể xảy ra lỗi như thiếu dữ liệu hoặc nhiều message bị dính vào nhau.
Để tránh vấn đề này, hệ thống sử dụng cơ chế length-prefixed framing, nghĩa là mỗi message được gửi theo định dạng:

```
{
  [4 byte độ dài][dữ liệu JSON]
}
```



Trong đó:

4 byte đầu tiên dùng để lưu độ dài của message
phần sau là nội dung JSON đã được mã hóa bằng UTF-8

Cách làm này giúp server và client biết chính xác cần đọc bao nhiêu byte cho mỗi message.

### 4.1. Gửi message

Hàm send_message(sock, msg_dict) được dùng để gửi message qua socket.

Quy trình thực hiện gồm:

Chuyển message từ dict sang chuỗi JSON
Mã hóa chuỗi JSON thành UTF-8 bytes
Đóng gói độ dài của message vào 4 byte bằng struct.pack()
Gửi toàn bộ dữ liệu qua socket bằng sock.sendall()

Nếu xảy ra lỗi khi gửi, hệ thống sẽ in thông báo "Send error" và đóng socket.

### 4.2. Nhận message

Hàm recv_message(sock) được dùng để nhận message từ socket.

Quy trình thực hiện gồm:

Đọc 4 byte đầu tiên để xác định độ dài của message
Đọc tiếp đúng số byte của phần nội dung JSON
Giải mã dữ liệu từ bytes sang chuỗi UTF-8
Chuyển chuỗi JSON thành dict bằng decode_message()
Kiểm tra tính hợp lệ bằng validate_message()

Nếu dữ liệu JSON không hợp lệ, hàm sẽ trả về một message ERROR với nội dung như "Invalid JSON".
Nếu message sai định dạng hoặc thiếu thông tin bắt buộc, hệ thống cũng sẽ trả về ERROR.
Nếu kết nối bị đóng hoặc có lỗi khi nhận dữ liệu, hàm sẽ trả về None.

### 4.3. Đọc đủ số byte cần thiết

Do sock.recv() không đảm bảo sẽ trả về đủ dữ liệu chỉ trong một lần gọi, hệ thống sử dụng hàm recvall(sock, n) để đọc chính xác n byte.

Hàm này sẽ:

lặp liên tục để đọc dữ liệu từ socket
dừng khi đã nhận đủ số byte yêu cầu
trả về None nếu kết nối bị đóng giữa chừng

Hàm recvall() rất quan trọng vì nó đảm bảo message được nhận đầy đủ trước khi tiến hành giải mã và kiểm tra.

## 5. Kiểm tra tính hợp lệ của message (Validation)

Sau khi message được nhận và giải mã từ JSON, hệ thống sử dụng hàm validate_message() để kiểm tra xem dữ liệu có đúng định dạng giao thức hay không trước khi xử lý.

Việc kiểm tra bao gồm:

Kiểm tra kiểu dữ liệu: message phải là một đối tượng kiểu dict
Kiểm tra loại message: trường type phải thuộc các loại message được hệ thống hỗ trợ
Kiểm tra các trường bắt buộc: mỗi loại message phải có đầy đủ các field cần thiết theo định nghĩa của giao thức
Kiểm tra nội dung tin nhắn (content):
không được để trống
không được vượt quá độ dài tối đa cho phép

Nếu message không hợp lệ, hàm sẽ trả về trạng thái lỗi kèm theo nguyên nhân, ví dụ:

Unknown type
Thiếu field: sender
Content rỗng
Content quá dài

Nếu phát hiện lỗi, hệ thống sẽ không xử lý tiếp message đó mà tạo một message ERROR để phản hồi.
Nhờ bước kiểm tra này, hệ thống tránh được việc xử lý các message sai định dạng, thiếu dữ liệu hoặc có nội dung không hợp lệ, từ đó giúp giao tiếp giữa client và server ổn định và an toàn hơn.

## 6. Luồng hoạt động của giao thức

Luồng giao tiếp cơ bản của hệ thống chat diễn ra như sau:

Client kết nối đến server bằng TCP socket
Client gửi message LOGIN để đăng nhập với tên người dùng
Server kiểm tra tên người dùng:
nếu hợp lệ → gửi LOGIN_SUCCESS
nếu không hợp lệ → gửi LOGIN_FAIL
Sau khi đăng nhập thành công, client gửi JOIN để tham gia phòng chat
Server cập nhật và gửi danh sách người dùng online bằng USER_LIST
Sau đó client có thể:
gửi CHAT để nhắn tin công khai trong phòng chat
gửi PRIVATE để nhắn tin riêng cho một người dùng khác
Khi rời hệ thống, client gửi LEAVE
Server thông báo người dùng rời đi và cập nhật lại danh sách online

Luồng này giúp quá trình đăng nhập, gửi tin nhắn và quản lý người dùng được thực hiện rõ ràng, nhất quán và dễ mở rộng.
