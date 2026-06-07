import sqlite3
import os
from pathlib import Path

DATABASE_FILE = 'app.db'
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / DATABASE_FILE

def setup_database():
    if not os.path.exists(DATABASE_PATH):
        print(f"[*] ساخت دیتابیس: {DATABASE_FILE}")
        dbc = sqlite3.connect(DATABASE_PATH)
        cursor = dbc.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                description TEXT
            )
        ''')
        dbc.commit()
        dbc.close()
        print("[+] دیتابیس و جداول با موفقیت ساخته شد.")
    else:
        print(f"[!] دیتابیس {DATABASE_FILE} از قبل وجود دارد.")
        # حتی اگر دیتابیس وجود داشت، چک کن که جدول products ساخته شود
        dbc = sqlite3.connect(DATABASE_PATH)
        cursor = dbc.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                description TEXT
            )
        ''')
        dbc.commit()
        dbc.close()
        print("[+] جدول products بررسی/ساخته شد.")

if __name__ == '__main__':
    setup_database()