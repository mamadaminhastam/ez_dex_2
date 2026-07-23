import sqlite3
from core.db_utils import get_db_connection


def handle(data, user_id=None):
    email = (data.get('email', [''])[0]).strip()
    subject = (data.get('subject', [''])[0]).strip()
    message = (data.get('message', [''])[0]).strip()

    if not email or not subject or not message:
        return False, "ایمیل، موضوع و پیام الزامی است."

    conn = None
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO contact_messages (email, subject, message, user_id) VALUES (?,?,?,?)",
                     (email, subject, message, user_id))
        conn.commit()
        return True, "پیام شما با موفقیت ارسال شد."
    except sqlite3.Error as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
