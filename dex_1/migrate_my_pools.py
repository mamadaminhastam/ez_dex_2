import sqlite3

conn = sqlite3.connect('ezdex.db')
try:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_pools (
            user_id INTEGER,
            pool_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, pool_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (pool_id) REFERENCES liquidity_pools(id)
        )
    ''')
    conn.commit()
    print("✅ جدول user_pools ساخته شد.")
except sqlite3.OperationalError as e:
    print(f"⚠️ خطا: {e}")
finally:
    conn.close()
