import sqlite3
import os

# نام فایل دیتابیس (می‌توانید مسیر دلخواه بدهید)
DATABASE_FILE = 'dex.db'

def setup_database():
    """ایجاد دیتابیس و جداول مورد نیاز صرافی غیرمتمرکز"""
    
    # اتصال به دیتابیس (اگر فایل نباشد، ساخته می‌شود)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # 1. جدول users (کاربران／کیف پول‌ها)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            wallet_address TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. جدول contact_messages (پیام‌های تماس با ما)
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
    
    # 3. جدول liquidity_pools (استخرهای نقدینگی / محصولات)
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
    
    # (اختیاری) جدول tokens برای ذخیره متادیتای توکن‌ها
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
    
    print(f"['the {DATABASE_FILE}' created ")
    print("    tables: users, contact_messages, liquidity_pools, tokens")

if __name__ == '__main__':
    # اگر فایل دیتابیس از قبل موجود باشد، جداول جدید اضافه می‌شوند (IF NOT EXISTS)
    setup_database()