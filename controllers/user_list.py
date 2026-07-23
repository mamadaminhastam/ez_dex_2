from core.db_utils import get_db_connection


def handle():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, email, role, created_at FROM users ORDER BY id")
        return [dict(row) for row in cur.fetchall()]
    finally:
        if conn:
            conn.close()
