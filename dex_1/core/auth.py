# core/auth.py
import uuid
import sqlite3
from dex_1.core.db_utils import get_db_connection
from dex_1.core.cookie import get_cookie


def create_session(user_id):
    session_id = str(uuid.uuid4())
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO sessions (id, user_id) VALUES (?, ?)",
                     (session_id, user_id))
        conn.commit()
        return session_id
    finally:
        if conn:
            conn.close()


def get_user_by_session(session_id):
    if not session_id:
        return None
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT users.id, users.username, users.email, users.role
            FROM sessions
            JOIN users ON sessions.user_id = users.id
            WHERE sessions.id = ?
        """, (session_id,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        if conn:
            conn.close()


def get_current_user(headers):
    session_id = get_cookie(headers, 'session_id')
    return get_user_by_session(session_id) if session_id else None


def require_role(headers, roles):
    user = get_current_user(headers)
    if not user:
        return None
    if user['role'] not in roles:
        return None
    return user


def delete_session(session_id):
    """حذف رکورد سشن از دیتابیس"""
    if not session_id:
        return
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()
