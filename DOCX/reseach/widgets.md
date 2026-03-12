# Widgets (Các thành phần giao diện)

**Widgets** là các thành phần hiển thị trên cửa sổ GUI như nút, textbox, label,...

## Một số widget phổ biến trong CustomTkinter

| Widget | Chức năng |
|------|-----------|
| `CTkLabel` | Hiển thị text |
| `CTkButton` | Nút bấm |
| `CTkEntry` | Ô nhập dữ liệu |
| `CTkTextbox` | Vùng nhập text nhiều dòng |
| `CTkFrame` | Khung chứa widget khác |
| `CTkCheckBox` | Ô chọn |
| `CTkRadioButton` | Chọn một trong nhiều |
| `CTkComboBox` | Danh sách chọn |
| `CTkSlider` | Thanh kéo |
| `CTkProgressBar` | Thanh tiến trình |
| `CTkSwitch` | Công tắc bật / tắt |
## Ví dụ sử dụng widgets

```python
import customtkinter as ctk

# tạo cửa sổ chính
app = ctk.CTk()

# label
label = ctk.CTkLabel(app, text="Hello CustomTkinter")
label.pack(pady=10)

# button
button = ctk.CTkButton(app, text="Click me")
button.pack(pady=10)

# entry
entry = ctk.CTkEntry(app, placeholder_text="Nhập text...")
entry.pack(pady=10)

# chạy ứng dụng
app.mainloop()
```