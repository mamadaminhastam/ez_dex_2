import sqlite3
import settings


def get_db_connection():
    """ایجاد اتصال امن به دیتابیس"""
    conn = sqlite3.connect(str(settings.DB_PATH), timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn
