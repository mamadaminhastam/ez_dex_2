import sqlite3      
from core.db_utils import get_db_connection


def handle(user_id, data):
    username = (data.get('username', [''])[0]).strip()
    email = (data.get('email', [''])[0]).strip()
    role = (data.get('role', ['user'])[0])

    if not username or not email:
        return False, "نام کاربری و ایمیل الزامی است."

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
        if cur.fetchone():
            return False, "این نام کاربری قبلاً استفاده شده است."
        cur.execute("UPDATE users SET username = ?, email = ?, role = ? WHERE id = ?",
                    (username, email, role, user_id))
        conn.commit()
        return True, "تغییرات با موفقیت ذخیره شد."
    except sqlite3.Error as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
