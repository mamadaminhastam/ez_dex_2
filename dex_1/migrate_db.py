# dex_1/migrate_db.py
import sqlite3

DATABASE_FILE = 'dex.db'

conn = sqlite3.connect(DATABASE_FILE)
conn.execute("PRAGMA foreign_keys=OFF;")
conn.execute("PRAGMA journal_mode=WAL;")

# 1. تغییر creator_wallet به صورت اختیاری
# چون SQLite اجازه ALTER COLUMN را ندارد، باید جدول را بازسازی کنیم:
conn.execute("ALTER TABLE liquidity_pools RENAME TO old_liquidity_pools;")

conn.execute('''
    CREATE TABLE liquidity_pools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token0_address TEXT NOT NULL,
        token1_address TEXT NOT NULL,
        token0_symbol TEXT,
        token1_symbol TEXT,
        initial_rate TEXT NOT NULL,
        initial_liquidity TEXT,
        creator_wallet TEXT,   -- NOT NULL حذف شد
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (creator_wallet) REFERENCES users(wallet_address) ON DELETE SET NULL
    )
''')

# کپی داده‌های موجود
conn.execute('''
    INSERT INTO liquidity_pools 
    SELECT * FROM old_liquidity_pools
''')

# حذف جدول قدیمی
conn.execute("DROP TABLE old_liquidity_pools;")

conn.execute("PRAGMA foreign_keys=ON;")
conn.commit()
conn.close()
print("✅ ستون creator_wallet اکنون NULL را می‌پذیرد.")
