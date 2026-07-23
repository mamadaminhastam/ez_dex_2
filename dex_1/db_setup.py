# db_setup.py
import sqlite3
import os

DATABASE_FILE = 'ezdex.db'


def setup_database():
    if os.path.exists(DATABASE_FILE):
        print(
            f"[!] دیتابیس {DATABASE_FILE} از قبل وجود دارد. برای بازنشانی آن را پاک کنید.")
        return

    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cur.execute('''
        CREATE TABLE contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE liquidity_pools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token0_address TEXT NOT NULL,
            token1_address TEXT NOT NULL,
            token0_symbol TEXT,
            token1_symbol TEXT,
            initial_rate TEXT NOT NULL,
            initial_liquidity TEXT,
            creator_id INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"[✓] دیتابیس '{DATABASE_FILE}' با موفقیت ساخته شد.")


if __name__ == '__main__':
    setup_database()
