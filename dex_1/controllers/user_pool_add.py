# controllers/user_pool_add.py
from dex_1.core.db_utils import get_db_connection


def handle(user_id, pool_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # چک کن که قبلاً اضافه نشده باشد
        cur.execute(
            "SELECT 1 FROM user_pools WHERE user_id = ? AND pool_id = ?", (user_id, pool_id))
        if cur.fetchone():
            return False, "این استخر قبلاً به لیست شما اضافه شده است."
        cur.execute(
            "INSERT INTO user_pools (user_id, pool_id) VALUES (?, ?)", (user_id, pool_id))
        conn.commit()
        return True, "استخر با موفقیت به My Pools اضافه شد."
    except Exception as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
