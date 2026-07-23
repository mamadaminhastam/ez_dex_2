# core/db_utils.py
import sqlite3
import settings


def get_db_connection():
    conn = sqlite3.connect(settings.DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn
