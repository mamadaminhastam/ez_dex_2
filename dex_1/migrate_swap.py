# migrate_swap.py
import sqlite3

conn = sqlite3.connect('ezdex.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pool_id INTEGER NOT NULL,
        from_token TEXT NOT NULL,
        to_token TEXT NOT NULL,
        from_amount TEXT NOT NULL,
        to_amount TEXT NOT NULL,
        rate TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (pool_id) REFERENCES liquidity_pools(id)
    )
''')
conn.commit()
conn.close()
print("✅ جدول transactions ساخته شد.")
