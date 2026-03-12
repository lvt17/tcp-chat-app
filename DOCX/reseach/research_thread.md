# Reseach chạy socket trên thread riêng không block main thread

Để có thể cho server nhận được cùng lúc nhiều client thì chúng ta phải cho mỗi client chạy trên 1 thread riêng biệt, lúc này hoạt động của client sẽ không gây ảnh hưởng đến luồng hoạt động chính của server 
dưới đây là cách thực hiện.

Ví dụ: ta có 1 hàm `def handle_client():`, hàm này sẽ được sử dụng để nhận dữ liệu từ client, từ đó decode và in ra thông tin mà user muốn gửi.

Khi `server_socket.listen()` và đã kết nối thành công nhận được object socket của client cũng như nhận thông tin như ip và port của client sau đó ta có thể tạo 1 luồng thread riêng cho từng server như đoạn code dưới đây.



```python
while True:  
    # Vòng lặp vô hạn, server sẽ luôn chạy để chấp nhận nhiều kết nối từ client

    conn, addr = server.accept()  
    # Chờ một client kết nối đến.
    # Khi có kết nối, trả về:
    #   conn: socket riêng để giao tiếp với client
    #   addr: địa chỉ (IP, port) của client

    thread = threading.Thread(target=handle_client, args=(conn, addr))  
    # Tạo một luồng (thread) mới để xử lý client vừa kết nối.
    # Hàm handle_client sẽ chạy trong luồng này, nhận tham số conn và addr.

    thread.start()  
    # Bắt đầu chạy luồng mới.
    # Nhờ vậy server có thể tiếp tục lắng nghe các kết nối khác song song,
    # không bị chặn bởi một client duy nhất.
```
