import customtkinter as ctk
import prototype_client
import threading
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(1.0)   
ctk.set_window_scaling(1.0)   

class ChatApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Chat Client")
        self.geometry("1100x700")

        self.client = None
        self.username = None
        self.selected_user = None
        self.is_auto_scrolling = False
        self.user_colors = {}

        self.show_login()  
    
    # ================= LOGIN =================

    def show_login(self):

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        title = ctk.CTkLabel(
            frame,
            text="💬 Chat Client",
            font=("Arial", 34, "bold")
        )
        title.pack(pady=40)

        self.username_entry = ctk.CTkEntry(
            frame,
            width=300,
            placeholder_text="Username"
        )
        self.username_entry.pack(pady=10)

        self.ip_entry = ctk.CTkEntry(
            frame,
            width=300,
            placeholder_text="Server IP"
        )
        self.ip_entry.pack(pady=10)

        find_btn = ctk.CTkButton(
            frame,
            text="Find Server",
            width=200,
            fg_color="#555555",
            command=self.auto_find_server
        )
        find_btn.pack(pady=5)

        btn = ctk.CTkButton(
            frame,
            text="CONNECT",
            width=200,
            command=self.connect
        )
        btn.pack(pady=20)

        self.username_entry.bind("<Return>", lambda e: self.connect())
        self.ip_entry.bind("<Return>", lambda e: self.connect())

    # ================= AUTO FIND =================

    def auto_find_server(self):
        """Tim server tren LAN bang UDP broadcast."""
        import threading

        def _find():
            result = prototype_client.discover_server(timeout=3)
            if result:
                ip, port = result
                self.after(0, lambda: self._fill_ip(ip))
            else:
                self.after(0, lambda: self._fill_ip("Khong tim thay"))

        self.ip_entry.delete(0, "end")
        self.ip_entry.insert(0, "Dang tim...")
        threading.Thread(target=_find, daemon=True).start()

    def _fill_ip(self, ip):
        self.ip_entry.delete(0, "end")
        self.ip_entry.insert(0, ip)

    # ================= CONNECT =================

    def connect(self):

        username = self.username_entry.get()
        ip = self.ip_entry.get()

        if username == "" or ip == "":
            return

        client = prototype_client.connect_to_server(
            ip,
            prototype_client.DEFAULT_PORT
        )

        if not client:
            return

        self.client = client
        self.username = username

        prototype_client.send_message(
            self.client,
            prototype_client.login(username)
        )

        threading.Thread(
            target=prototype_client.recieve_loop,
            args=(self.client, username),
            daemon=True
        ).start()

        for w in self.winfo_children():
            w.destroy()

        self.build_chat_ui()

        self.after(100, self.update_messages)

    # ================= CHAT UI =================

    def build_chat_ui(self):

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="CHAT ROOM",
            font=("Arial", 24, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # CHAT AREA
        self.chat_area = ctk.CTkScrollableFrame(self)
        self.chat_area.grid(
            row=1, column=0,
            padx=10, pady=10,
            sticky="nsew"
        )

        # USER LIST
        self.user_frame = ctk.CTkFrame(self)
        self.user_frame.grid(
            row=1, column=1,
            padx=10, pady=10,
            sticky="nsew"
        )

        label = ctk.CTkLabel(
            self.user_frame,
            text="ONLINE USERS",
            font=("Arial", 18, "bold")
        )
        label.pack(pady=10)

        btn = ctk.CTkButton(
            self.user_frame,
            text="🌐 Public Chat",
            command=self.public_chat
        )
        btn.pack(fill="x", padx=5, pady=5)

        self.user_buttons = {}

        # INPUT
        self.message_entry = ctk.CTkEntry(
            self,
            placeholder_text="Type message..."
        )
        self.message_entry.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.message_entry.bind("<Return>", lambda e: self.send_message())

        send_btn = ctk.CTkButton(
            self,
            text="Send",
            command=self.send_message
        )
        send_btn.grid(row=2, column=1)

        disconnect = ctk.CTkButton(
            self,
            text="Disconnect",
            fg_color="red",
            command=self.disconnect
        )
        disconnect.grid(row=3, column=1, pady=10)

        self.public_chat()

    # ================= CHAT BUBBLE =================

    def create_bubble(self, sender, text, private=False):
        if not self.chat_area.winfo_exists():
            return
        # Xác định xem đây là tin nhắn của mình hay người khác
        is_me = (sender == self.username)
        # Căn lề: 'e' bên phải cho mình, 'w' (West) bên trái cho người khác
        side = "e" if is_me else "w"
        
        # Frame tổng chứa toàn bộ cụm tin nhắn
        frame = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        frame.pack(anchor=side, pady=5, padx=10, fill="x")

        # Nội dung bên trong (dùng frame phụ để bọc sát nội dung)
        bubble_container = ctk.CTkFrame(frame, fg_color="transparent")
        bubble_container.pack(anchor=side)

        # Header (Tên & Thời gian)
        color = self.get_user_color(sender)
        header_text = f"{sender}  {datetime.now().strftime('%H:%M')}"
        
        header = ctk.CTkLabel(
            bubble_container,
            text=header_text,
            text_color=color,
            font=("Segoe UI", 11, "bold")
        )
        header.pack(anchor=side, padx=5)

        # Màu sắc bong bóng
        if private:
            bubble_color = "#a855f7" # Tím cho tin nhắn riêng
        else:
            bubble_color = "#2b7cff" if is_me else "#333333"

        # Nội dung tin nhắn
        msg = ctk.CTkLabel(
            bubble_container,
            text=text,
            wraplength=400,
            fg_color=bubble_color,
            text_color="white",
            corner_radius=15,
            padx=12,
            pady=8,
            font=("Segoe UI", 12)
        )
        msg.pack(anchor=side)
        self.after_idle(self.auto_scroll_if_needed)
    # ================= USER COLOR =================

    def get_user_color(self, user):

        if user not in self.user_colors:

            import random

            colors = [
                "#ff6b6b",
                "#4ecdc4",
                "#ffe66d",
                "#1a535c",
                "#ff9f1c",
                "#a29bfe"
            ]

            self.user_colors[user] = random.choice(colors)

        return self.user_colors[user]

    # ================= PUBLIC CHAT =================
    def public_chat(self):
        self.select_user(None)

    # ================= USER SELECT =================
    def select_user(self, user):

        # ===== chọn user =====
        self.selected_user = user

        # ===== highlight user đang chọn =====
        for u, btn in self.user_buttons.items():
            if u == user:
                btn.configure(fg_color="#1f6aa5")  # màu đang chọn
            else:
                btn.configure(fg_color=("gray75", "gray25")) # reset

        # ===== clear chat =====
        for widget in self.chat_area.winfo_children():
            widget.destroy()

        # ===== PRIVATE CHAT =====
        if user:

            # tiêu đề
            title = ctk.CTkLabel(
                self.chat_area,
                text=f"💬 Chat với {user}",
                font=("Arial", 16, "bold")
            )
            title.pack(pady=5)

            # render lịch sử
            if hasattr(self, "chat_history") and user in self.chat_history:

                for msg in self.chat_history[user]:
                    self.create_bubble(
                        msg["sender"],
                        msg["content"],
                        True
                    )

        # ===== PUBLIC CHAT =====
        else:

            # tiêu đề
            title = ctk.CTkLabel(
                self.chat_area,
                text="🌐 Public Chat",
                font=("Arial", 16, "bold")
            )
            title.pack(pady=5)

            # render lịch sử public
            if hasattr(self, "public_history"):

                for msg in self.public_history:
                    self.create_bubble(
                        msg["sender"],
                        msg["content"]
                    )
        self.after(100, self.scroll_to_bottom)
    # ================= UPDATE USER LIST =================

    def update_user_list(self, users):

        for btn in self.user_buttons.values():
            btn.destroy()

        self.user_buttons.clear()

        for user in users:
            if user == self.username:
                continue
            btn = ctk.CTkButton(
                self.user_frame,
                text="🟢 " + user,
                anchor="w",
                command=lambda u=user: self.select_user(u)
            )

            btn.pack(fill="x", padx=5, pady=3)

            self.user_buttons[user] = btn

    # ================= SEND =================

    def send_message(self):

        msg = self.message_entry.get()

        if msg == "":
            return
        # ===== PRIVATE =====
        if self.selected_user:
            prototype_client.send_message(
                self.client,
                prototype_client.private(
                    self.username,
                    self.selected_user,
                    msg
                )
            )      
        # ===== PUBLIC =====
        else:
            prototype_client.send_message(
                self.client,
                prototype_client.chat(
                    self.username,
                    msg
                )
            )

        self.message_entry.delete(0, "end")

    # ================= UPDATE MESSAGE =================

    def update_messages(self):
        if not hasattr(self, "chat_area") or not self.chat_area.winfo_exists():
            return

        while not prototype_client.msg_queue.empty():

            msg = prototype_client.msg_queue.get()
            msg_type = msg.get("type")

            # ===== PUBLIC CHAT =====
            if msg_type == "CHAT":

                # lưu history
                if not hasattr(self, "public_history"):
                    self.public_history = []

                self.public_history.append(msg)

                # chỉ hiển thị khi đang ở public
                if self.selected_user is None:

                    self.create_bubble(
                        msg["sender"],
                        msg["content"]
                    )
            # ===== PRIVATE CHAT =====
            elif msg_type == "PRIVATE":

                sender = msg.get("sender")
                receiver = msg.get("receiver")

                # chỉ xử lý nếu liên quan tới mình
                if sender == self.username or receiver == self.username:

                    other_user = receiver if sender == self.username else sender

                    # lưu history
                    if not hasattr(self, "chat_history"):
                        self.chat_history = {}

                    if other_user not in self.chat_history:
                        self.chat_history[other_user] = []

                    self.chat_history[other_user].append(msg)

                    # chỉ hiển thị khi đang mở đúng người
                    if self.selected_user == other_user:

                        self.create_bubble(
                            sender,
                            msg["content"],
                            True,
                        )
            # ===== SYSTEM =====
            elif msg_type == "SYSTEM":

                self.create_bubble(
                    "SYSTEM",
                    msg["content"]
                )
            # ===== USER LIST =====
            elif msg_type == "USER_LIST":

                self.update_user_list(msg["users"])

        self.update_job = self.after(100, self.update_messages)
    # ================== Scroll ===================
    def scroll_to_bottom(self):

        if not hasattr(self, "chat_area"):
            return

        canvas = self.chat_area._parent_canvas

        self.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(1.0)


    def smooth_scroll_to_bottom(self):

        if self.is_auto_scrolling:
            return

        canvas = self.chat_area._parent_canvas

        top, bottom = canvas.yview()

        if bottom < 0.92:
            return

        self.is_auto_scrolling = True

        start = top
        end = 1.0
        steps = 8
        delta = (end - start) / steps

        def animate(step=0):
            if step >= steps:
                canvas.yview_moveto(1.0)
                self.is_auto_scrolling = False
                return

            canvas.yview_moveto(start + delta * step)
            self.after(12, lambda: animate(step + 1))

        animate()


    def auto_scroll_if_needed(self):
        if not hasattr(self, "chat_area"):
            return

        canvas = self.chat_area._parent_canvas
        canvas.configure(scrollregion=canvas.bbox("all"))

        top, bottom = canvas.yview()

        if bottom > 0.90:
            self.smooth_scroll_to_bottom()

    # ================= DISCONNECT =================

    def disconnect(self):

        if hasattr(self, "update_job"):
            try:
                self.after_cancel(self.update_job)
            except:
                pass

        if self.client:
            prototype_client.disconnect(
                self.client,
                self.username
            )
            self.client = None

        self.selected_user = None

        if hasattr(self, "chat_history"):
            self.chat_history.clear()

        if hasattr(self, "public_history"):
            self.public_history.clear()

        for w in self.winfo_children():
            w.destroy()

        self.show_login()


app = ChatApp()
app.mainloop()