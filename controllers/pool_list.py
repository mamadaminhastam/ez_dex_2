from core.db_utils import get_db_connection


# controllers/pool_list.py
def handle(only_active=False, include_deleted=False):
    conn = get_db_connection()
    query = "SELECT id, token0_symbol, token1_symbol, initial_rate, initial_liquidity, is_active, is_deleted, creator_id FROM liquidity_pools WHERE 1=1"
    if not include_deleted:
        query += " AND is_deleted = 0"
    if only_active:
        query += " AND is_active = 1"
    query += " ORDER BY created_at DESC"
    cur = conn.cursor()
    cur.execute(query)
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results
