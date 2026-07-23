import sqlite3
from dex_1.core.db_utils import get_db_connection


def handle(pool_id, data):
    token0_address = (data.get('token0_address', [''])[0]).strip()
    token1_address = (data.get('token1_address', [''])[0]).strip()
    token0_symbol = (data.get('token0_symbol', [''])[0]).strip() or None
    token1_symbol = (data.get('token1_symbol', [''])[0]).strip() or None
    initial_rate = (data.get('initial_rate', [''])[0]).strip()
    initial_liquidity = (data.get('initial_liquidity', [''])[
                         0]).strip() or None
    is_active = int(data.get('is_active', ['1'])[0])

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""UPDATE liquidity_pools SET token0_address=?, token1_address=?, token0_symbol=?, token1_symbol=?,
                       initial_rate=?, initial_liquidity=?, is_active=? WHERE id=?""",
                    (token0_address, token1_address, token0_symbol, token1_symbol, initial_rate, initial_liquidity, is_active, pool_id))
        conn.commit()
        return True, "استخر ویرایش شد."
    except sqlite3.Error as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
