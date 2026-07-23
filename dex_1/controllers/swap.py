# controllers/swap.py
from dex_1.core.db_utils import get_db_connection


def get_pools():
    """برگرداندن لیست استخرهای فعال برای dropdown"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, token0_symbol, token1_symbol, initial_rate FROM liquidity_pools WHERE is_deleted=0 AND is_active=1")
    pools = [dict(row) for row in cur.fetchall()]
    conn.close()
    return pools


def perform_swap(user_id, pool_id, from_token, to_token, amount_str, rate_str):
    """انجام مبادله و ثبت در تاریخچه"""
    if not amount_str:
        return False, "مقدار ورودی الزامی است."
    try:
        amount = float(amount_str)
    except ValueError:
        return False, "مقدار باید عددی باشد."

    # استخراج نرخ از رشته‌ای مانند "1 ETH = 3000 USDC"
    rate_parts = rate_str.split("=")
    if len(rate_parts) != 2:
        return False, "فرمت نرخ معتبر نیست."
    try:
        to_rate = float(rate_parts[1].strip().split()[0])
    except (ValueError, IndexError):
        return False, "نرخ نامعتبر است."

    to_amount = amount * to_rate

    conn = None
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO transactions (user_id, pool_id, from_token, to_token, from_amount, to_amount, rate) VALUES (?,?,?,?,?,?,?)",
            (user_id, pool_id, from_token, to_token,
             str(amount), str(to_amount), rate_str)
        )
        conn.commit()
        return True, f"مبادله موفق: {amount} {from_token} → {to_amount:.4f} {to_token}"
    except Exception as e:
        return False, f"خطا: {str(e)}"
    finally:
        if conn:
            conn.close()
