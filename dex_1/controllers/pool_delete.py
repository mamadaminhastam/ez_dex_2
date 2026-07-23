# controllers/pool_delete.py
from dex_1.core.db_utils import get_db_connection


def handle(pool_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE liquidity_pools SET is_deleted = 1 WHERE id = ?", (pool_id,))
        if cur.rowcount == 0:
            return False, "استخر یافت نشد."
        conn.commit()
        return True, "استخر با موفقیت حذف شد."
    except Exception as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
