from dex_1.core.db_utils import get_db_connection


def handle():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, subject, message, user_id, created_at FROM contact_messages ORDER BY created_at DESC")
        return [dict(row) for row in cur.fetchall()]
    finally:
        if conn:
            conn.close()
