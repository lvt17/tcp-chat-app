# Kịch bản kiểm thử (Test Cases) - Nhóm 6
Các bước kiểm thử bao gồm:
| STT | Tên Test Case | Thao tác | Kết quả mong đợi |
|:---:|:---|:---|:---|
| 1 | Kết nối đơn lẻ | Nhấn "Connect" trên 1 Client | Server báo nhận kết nối; Client sẵn sàng Login |
| 2 | Kết nối đồng thời | Mở 2+ Client cùng kết nối | Server xử lý đa luồng (Multi-thread) ổn định |
| 3 | Đúng định dạng | Gửi tin nhắn bất kỳ | Server nhận đúng: `[LOẠI] [SENDER] [RECEIVER] [CONTENT] [TIME]` |
| 4 | Phát tin (Broadcast) | Client A gửi tin nhắn | Client B và C nhận được tin nhắn ngay lập tức |
| 5 | Ngắt kết nối | Nhấn "Disconnect" hoặc đóng App | Server xóa tên khỏi list Online; Đóng Socket an toàn |
