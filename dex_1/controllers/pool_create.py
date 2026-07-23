import sqlite3
from dex_1.core.db_utils import get_db_connection


def handle(data, user_id=None):
    token0_address = (data.get('token0_address', [''])[0]).strip()
    token1_address = (data.get('token1_address', [''])[0]).strip()
    token0_symbol = (data.get('token0_symbol', [''])[0]).strip() or None
    token1_symbol = (data.get('token1_symbol', [''])[0]).strip() or None
    initial_rate = (data.get('initial_rate', [''])[0]).strip()
    initial_liquidity = (data.get('initial_liquidity', [''])[
                         0]).strip() or None

    if not token0_address or not token1_address or not initial_rate:
        return False, "آدرس دو توکن و نرخ اولیه الزامی است."

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO liquidity_pools 
            (token0_address, token1_address, token0_symbol, token1_symbol, initial_rate, initial_liquidity, creator_id)
            VALUES (?,?,?,?,?,?,?)""",
                    (token0_address, token1_address, token0_symbol, token1_symbol, initial_rate, initial_liquidity, user_id))
        conn.commit()
        return True, "استخر با موفقیت ایجاد شد."
    except sqlite3.Error as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
