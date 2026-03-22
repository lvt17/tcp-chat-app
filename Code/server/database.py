import sqlite3
import threading

DB_PATH = "chat_history.db"
db_lock = threading.Lock()


def init_db():
    """Tao bang messages neu chua ton tai."""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                receiver TEXT DEFAULT NULL
            )
        """)
        conn.commit()
        conn.close()


def save_message(sender, content, timestamp, receiver=None):
    """Luu 1 tin nhan vao database. receiver=None la tin public."""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (sender, content, timestamp, receiver) VALUES (?, ?, ?, ?)",
            (sender, content, timestamp, receiver)
        )
        conn.commit()
        conn.close()


def get_recent_messages(limit=50):
    """Lay N tin nhan gan nhat (chi tin public)."""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sender, content, timestamp, receiver FROM messages "
            "WHERE receiver IS NULL "
            "ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()

    # dao nguoc de tin cu len truoc
    rows.reverse()
    return [
        {"sender": r[0], "content": r[1], "timestamp": r[2], "receiver": r[3]}
        for r in rows
    ]
