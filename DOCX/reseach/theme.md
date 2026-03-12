# Theme (Giao diện màu sắc)

CustomTkinter hỗ trợ Dark mode và Light mode.

## Chọn chế độ giao diện

```python
ctk.set_appearance_mode("dark")   # dark / light / system
```

## Chọn theme màu

```python
ctk.set_default_color_theme("blue")
```
**theme có sẵn**

| Theme | Mô tả |
|------|------|
| `blue` | mặc định |
| `green` | màu xanh lá |
| `dark-blue` | xanh đậm |

## Ví dụ
```python
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")

button = ctk.CTkButton(app, text="Button")
button.pack(pady=20)

app.mainloop()
```