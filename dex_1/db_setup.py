# dex_1/db_setup.py
import sqlite3
import os

DATABASE_FILE = 'dex.db'

def setup_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # users با کلید اصلی id و wallet_address اختیاری
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT UNIQUE,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            wallet_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liquidity_pools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token0_address TEXT NOT NULL,
            token1_address TEXT NOT NULL,
            token0_symbol TEXT,
            token1_symbol TEXT,
            initial_rate TEXT NOT NULL,
            initial_liquidity TEXT,
            creator_wallet TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_wallet) REFERENCES users(wallet_address) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            address TEXT PRIMARY KEY,
            symbol TEXT NOT NULL,
            name TEXT,
            decimals INTEGER DEFAULT 18,
            added_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print(f"[✓] دیتابیس '{DATABASE_FILE}' با جداول جدید ساخته شد.")

if __name__ == '__main__':
    setup_database()