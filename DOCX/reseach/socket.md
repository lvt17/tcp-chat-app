# Reseach connect, send, recv

## connect()
***Kết nối socket của client đến socket của server***
 `client_socket.connect((IP, PORT))`

 ## send()
 ***Gửi dữ liệu giữa server và client dưới dạng bytes***
 Nếu muốn gửi thông điệp dưới dạng chữ ABC thì bắt buộc phải encode thành kiểu bytes mới gửi được giữa các socket.

 Ví dụ `msg = "hello"`
`message = msg.encode("utf-8")`(utf-8 là chuẩn mã hóa dùng để chuyển đổi ngôn ngữ)
 `client_socket.send(message)`

 ## recv()
 ***Nhận dữ liệu giữa server và client dưới dạng bytes***
sau khi nhận thông điệp dưới dạng bytes thì client/server phải decode mới nhận được thông điệp mà user muốn gửi.

ví dụ `data = server_socket.recv(bufsize)` (bufsize là số bytes tối đa socket có thể nhận trong 1 lần gửi dữ liệu)

sau khi nhận thì có thể decode để in ra dữ liệu.
ví dụ `print(data.decode("utf-8"))`

