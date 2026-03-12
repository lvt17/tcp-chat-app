# Nghiên cứu: Kết nối Network Thread với GUI Thread bằng Queue

Trong các ứng dụng có giao diện đồ họa (GUI), việc xử lý dữ liệu mạng thường được thực hiện ở **network thread** để tránh làm treo giao diện. Tuy nhiên, GUI thread mới có quyền cập nhật trực tiếp giao diện. Do đó, cần một cơ chế an toàn để truyền dữ liệu từ network thread sang GUI thread.  
**Queue** là giải pháp phổ biến vì đảm bảo luồng dữ liệu tuần tự, tránh xung đột và dễ quản lý.

## 2. Mô hình hoạt động
- **Network Thread**: 
  - Lắng nghe dữ liệu từ socket/server.
  - Đưa dữ liệu nhận được vào **queue**.
- **GUI Thread**: 
  - Định kỳ kiểm tra queue.
  - Lấy dữ liệu ra và cập nhật giao diện.

Sơ đồ: [Network Thread] ---> [Queue] ---> [GUI Thread]

