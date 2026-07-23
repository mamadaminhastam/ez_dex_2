import sqlite3
import hashlib
from dex_1.core.db_utils import get_db_connection


def handle(data):
    username = (data.get('username', [''])[0]).strip()
    email = (data.get('email', [''])[0]).strip()
    password = (data.get('password', [''])[0])
    password_confirm = (data.get('password_confirm', [''])[0])

    if not username or not email or not password:
        return False, "نام کاربری، ایمیل و رمز عبور الزامی است."
    if password != password_confirm:
        return False, "رمز عبور و تکرار آن مطابقت ندارند."
    if not username.replace('_', '').isalnum():
        return False, "نام کاربری فقط حروف انگلیسی، اعداد و زیرخط مجاز است."

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            return False, "این نام کاربری قبلاً ثبت شده است."
        cur.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, 'user')",
                    (username, email, password_hash))
        conn.commit()
        return True, "ثبت‌نام با موفقیت انجام شد. حالا می‌توانید وارد شوید."
    except sqlite3.Error as e:
        return False, f"خطای دیتابیس: {str(e)}"
    finally:
        if conn:
            conn.close()
