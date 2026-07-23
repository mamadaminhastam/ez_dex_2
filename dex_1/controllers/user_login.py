import hashlib
from dex_1.core.db_utils import get_db_connection
from dex_1.core import auth


def handle(data):
    username = (data.get('username', [''])[0]).strip()
    password = (data.get('password', [''])[0])

    if not username or not password:
        return None, "نام کاربری و رمز عبور الزامی است."

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, role FROM users WHERE username = ? AND password_hash = ?",
                    (username, password_hash))
        row = cur.fetchone()
        if row:
            user = dict(row)
            session_id = auth.create_session(user['id'])
            return user, session_id
        return None, "نام کاربری یا رمز عبور اشتباه است."
    finally:
        if conn:
            conn.close()
