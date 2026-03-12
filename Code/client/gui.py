import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Chat Client")
        self.geometry("900x600")

        self.selected_user = None

        self.show_login()

    # ================= LOGIN SCREEN =================
    def show_login(self):

        bg_frame = ctk.CTkFrame(self, fg_color="transparent")
        bg_frame.pack(expand=True)

        self.login_frame = ctk.CTkFrame(
            bg_frame,
            width=450,
            height=420,
            corner_radius=20
        )
        self.login_frame.pack(expand=True)

        title = ctk.CTkLabel(
            self.login_frame,
            text="💬 CHAT CLIENT",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.login_frame,
            text="Realtime Socket Messaging",
            font=("Arial", 16),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 25))

        username_label = ctk.CTkLabel(
            self.login_frame,
            text="Username",
            font=("Arial", 20)
        )
        username_label.pack()

        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            width=320,
            height=42,
            corner_radius=10,
            placeholder_text="Enter username"
        )
        self.username_entry.pack(pady=10)

        ip_label = ctk.CTkLabel(
            self.login_frame,
            text="Server IP",
            font=("Arial", 20)
        )
        ip_label.pack()

        self.ip_entry = ctk.CTkEntry(
            self.login_frame,
            width=320,
            height=42,
            corner_radius=10,
            placeholder_text="127.0.0.1"
        )
        self.ip_entry.pack(pady=10)

        connect_btn = ctk.CTkButton(
            self.login_frame,
            text="🚀 CONNECT",
            width=260,
            height=50,
            corner_radius=12,
            font=("Arial", 18, "bold"),
            command=self.connect
        )
        connect_btn.pack(pady=30)

        self.username_entry.bind("<Return>", lambda event: self.connect())
        self.ip_entry.bind("<Return>", lambda event: self.connect())

    # ================= CONNECT =================
    def connect(self):

        username = self.username_entry.get()
        server_ip = self.ip_entry.get()

        print("Username:", username)
        print("Server IP:", server_ip)

        # xóa login UI
        for widget in self.winfo_children():
            widget.destroy()

        # mở chat UI
        self.show_chat()

    # ================= CHAT SCREEN =================
    def show_chat(self):

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self,
                             text="CHAT ROOM",
                             font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # ===== Chat Box =====
        self.chat_box = ctk.CTkTextbox(self,
                                       corner_radius=10,
                                       font=("Arial", 14))
        self.chat_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.chat_box.configure(state="disabled")

        # ===== User List =====
        self.user_frame = ctk.CTkFrame(self)
        self.user_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        user_title = ctk.CTkLabel(self.user_frame,
                                  text="ONLINE USERS",
                                  font=("Arial", 16, "bold"))
        user_title.pack(pady=10)

        public_btn = ctk.CTkButton(
            self.user_frame,
            text="🌐 Public Chat",
            fg_color="gray",
            command=self.public_chat
        )
        public_btn.pack(fill="x", padx=5, pady=5)

        self.users = ["user1", "user2", "user3"]

        for user in self.users:

            btn = ctk.CTkButton(self.user_frame,
                                text="● " + user,
                                anchor="w",
                                command=lambda u=user: self.select_user(u))

            btn.pack(fill="x", padx=5, pady=3)

        # ===== Message Input =====
        self.message_entry = ctk.CTkEntry(self,
                                          height=40,
                                          placeholder_text="Type message...")
        self.message_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.message_entry.bind("<Return>", lambda event: self.send_message())

        # ===== Send Button =====
        send_btn = ctk.CTkButton(self,
                                 text="Send",
                                 width=120,
                                 command=self.send_message)
        send_btn.grid(row=2, column=1, padx=10, pady=10)

        # ===== Disconnect Button =====
        disconnect_btn = ctk.CTkButton(self,
                                       text="Disconnect",
                                       fg_color="red",
                                       command=self.disconnect)
        disconnect_btn.grid(row=3, column=1, padx=10, pady=5)

    # ================= PUBLIC CHAT =================
    def public_chat(self):

        self.selected_user = None

        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", "--- Back to Public Chat ---\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    # ================= PRIVATE CHAT =================
    def select_user(self, user):

        self.selected_user = user

        self.chat_box.configure(state="normal")
        self.chat_box.insert("end",
                             f"--- Private chat with {user} ---\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    # ================= SEND MESSAGE =================
    def send_message(self):

        msg = self.message_entry.get()

        if msg != "":

            self.chat_box.configure(state="normal")

            if self.selected_user:
                self.chat_box.insert("end",
                                     f"Me -> {self.selected_user}: {msg}\n")
            else:
                self.chat_box.insert("end",
                                     f"Me (Public): {msg}\n")

            self.chat_box.see("end")
            self.chat_box.configure(state="disabled")

            self.message_entry.delete(0, "end")

    # ================= DISCONNECT =================
    def disconnect(self):

        print("Disconnected")

        for widget in self.winfo_children():
            widget.destroy()

        self.show_login()


# Run app
app = ChatApp()
app.mainloop()