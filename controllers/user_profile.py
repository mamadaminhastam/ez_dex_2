# controllers/user_profile.py
import hashlib
from core.db_utils import get_db_connection


def get_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        if conn:
            conn.close()


def update_profile(user_id, data):
    username = (data.get('username', [''])[0]).strip()
    email = (data.get('email', [''])[0]).strip()
    password = (data.get('password', [''])[0])
    password_confirm = (data.get('password_confirm', [''])[0])

    if not username or not email:
        return False, "نام کاربری و ایمیل الزامی است."

    # اگر رمزی وارد شده باشد، بررسی تطابق و به‌روزرسانی
    password_hash = None
    if password:
        if password != password_confirm:
            return False, "رمز عبور و تکرار آن مطابقت ندارند."
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # یکتایی نام کاربری (به جز خود کاربر)
        cur.execute(
            "SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
        if cur.fetchone():
            return False, "این نام کاربری قبلاً استفاده شده است."

        if password_hash:
            cur.execute("UPDATE users SET username = ?, email = ?, password_hash = ? WHERE id = ?",
                        (username, email, password_hash, user_id))
        else:
            cur.execute("UPDATE users SET username = ?, email = ? WHERE id = ?",
                        (username, email, user_id))
        conn.commit()
        return True, "اطلاعات با موفقیت به‌روز شد."
    except Exception as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
