# TCP socket research:

## blind() 
***Gán socket với port***
syntax: `server_socket.bind(IP, PORT)`

## listen()
 ***Chỉ dùng cho TCP server. Sau khi bind xong → server mở cổng chờ kết nối.***

 ví dụ: `listen(5)`: 5 = backlog → tối đa 5 request connect đang chờ.

 ## accept()
 Khi client connect, OS sẽ tạo 1 socket mới riêng hoang toàn cho client

 ## Cấu trúc socket:
***1 server - N client***

## Flow socket cho project hiện tại:
***Server:***
`socket → bind → listen → accept → recv/send`
```python
socket()
bind(8080)
listen()

while true:
    client = accept()
    recv()
    send()
```

***Client:***
`socket → connect → recv/send`
```python
socket()
connect(server_ip, 8080)
send()
recv()
```
