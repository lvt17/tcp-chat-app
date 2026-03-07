# Ứng dụng trò chuyện GUI qua TCP (Python)

Dự án xây dựng một hệ thống Chat Client-Server sử dụng giao thức TCP, hỗ trợ đa luồng và giao diện người dùng hiện đại với thư viện CustomTkinter.

## 📋 Thành phần dự án
- **client/**: Chứa mã nguồn giao diện (GUI) và logic kết nối phía người dùng.
- **server/**: Bộ trung tâm xử lý kết nối, điều phối tin nhắn (Message Broker) và quản lý người dùng online.
- **shared/**: Định nghĩa cấu trúc gói tin chung (`protocol.py`) để đồng bộ giữa Client và Server.

## 🔄 Luồng hoạt động chính
1. **Connect**: Client thiết lập kết nối tới Server qua Socket TCP.
2. **Login**: Client gửi định danh; Server xác nhận và cập nhật danh sách trực tuyến.
3. **Chat**: Tin nhắn được gửi đến Server và chuyển tiếp (Broadcast) tới tất cả thành viên.
4. **Disconnect**: Ngắt kết nối và giải phóng tài nguyên hệ thống.

## 🛠 Yêu cầu và Khởi chạy
- **Ngôn ngữ**: Python 3.x.
- **Thư viện**: `customtkinter` (Khai báo trong `requirements.txt`).
- **Cài đặt**: `pip install -r requirements.txt`.
- **Chạy ứng dụng**: Chạy `server/server.py` trước, sau đó chạy `client/gui.py`.
