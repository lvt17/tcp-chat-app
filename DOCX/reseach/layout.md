# Layouts (Bố trí giao diện)

**Layout** dùng để sắp xếp vị trí widget trong cửa sổ.

CustomTkinter kế thừa layout của Tkinter gồm 3 loại chính.

## Các loại layout

### 1.pack()

Sắp xếp widget theo chiều dọc hoặc ngang.

```python
label.pack(pady=10)
button.pack(pady=10)
```
**Thuộc tính thường dùng**

| Thuộc tính | Ý nghĩa |
|-----------|--------|
| `padx` | Khoảng cách theo chiều ngang |
| `pady` | Khoảng cách theo chiều dọc |
| `side` | Vị trí widget (`left`, `right`, `top`, `bottom`) |
| `fill` | Mở rộng widget theo chiều ngang hoặc dọc |
| `expand` | Cho phép widget chiếm thêm không gian |

### 2.grid()

Bố trí theo hàng và cột.

```python
label.grid(row=0, column=0)
entry.grid(row=0, column=1)
button.grid(row=1, column=0, columnspan=2)
```

### 3.place()

Đặt widget theo tọa độ tuyệt đối.

```python
button.place(x=100, y=50)
```