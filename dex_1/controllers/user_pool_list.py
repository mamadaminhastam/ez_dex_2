# controllers/user_pool_list.py
from dex_1.core.db_utils import get_db_connection


def handle(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT l.id, l.token0_symbol, l.token1_symbol, l.initial_rate, l.initial_liquidity, l.is_active
            FROM user_pools u
            JOIN liquidity_pools l ON u.pool_id = l.id
            WHERE u.user_id = ? AND l.is_deleted = 0
            ORDER BY u.created_at DESC
        ''', (user_id,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        if conn:
            conn.close()
