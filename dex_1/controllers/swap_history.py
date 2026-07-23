# controllers/swap_history.py
from dex_1.core.db_utils import get_db_connection


def get_user_history(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, p.token0_symbol, p.token1_symbol, t.from_token, t.to_token,
               t.from_amount, t.to_amount, t.rate, t.created_at
        FROM transactions t
        JOIN liquidity_pools p ON t.pool_id = p.id
        WHERE t.user_id = ?
        ORDER BY t.created_at DESC
    """, (user_id,))
    history = [dict(row) for row in cur.fetchall()]
    conn.close()
    return history
