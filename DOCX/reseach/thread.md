# THREADING

***Threading cho phép một chương trình thực thi nhiều luồng công việc song song trong cùng một process. Trong các ứng dụng server, threading thường được dùng để xử lý nhiều client cùng lúc thay vì xử lý tuần tự từng request.***. Ví dụ một server không dùng threading, khi client gửi đồng loạt 3 request, nếu server không sử dụng threading, khi một client đang được xử lý thì server sẽ bị block và không thể phục vụ client khác cho đến khi xử lý xong. ***Nhưng với Threading*** thì nó sẽ cho mỗi request là 1 thread riêng biệt và xử lý chúng cùng lúc mà không ảnh hưởng đến nhau.

## Flow của một thread:

Flow xử lý client trong server:

accept client  
↓  
tạo thread mới  
↓  
thread xử lý client  
↓  
server quay lại accept client khác

## Daemon thread

***Thread nền***

Daemon thread là thread chạy nền. Khi chương trình chính kết thúc thì daemon thread cũng sẽ tự động kết thúc theo.

Daemon thread thường được dùng cho các tác vụ nền như luồng nhận tin nhắn (receive thread) trong client.

```python
thread = threading.Thread(target=listen, daemon=True)
thread.start()
```

## Lock

Lock được dùng khi nhiều thread cùng truy cập và thay đổi một tài nguyên chung (shared resource). 
Lock đảm bảo tại một thời điểm chỉ có một thread được phép truy cập tài nguyên đó, giúp tránh lỗi race condition.

```python
lock = threading.Lock()

with lock:
    clients.append(client)
```

## Thread model của project:

Server:

main thread  
↓  
accept client  
↓  
spawn thread  
↓  
handle_client()

Client:

main thread → xử lý GUI  
thread 1 → receive message  
thread 2 → send message

### Trong Python, module threading cho phép tạo và quản lý các thread trong chương trình. Mỗi client kết nối tới server thường được xử lý bởi một thread riêng biệt (thread-per-client model).