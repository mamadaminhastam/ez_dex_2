# user_add.py
import sqlite3
import os

DATABASE_FILE = "dex.db"

def add_user():
    # اطلاعات نمونه برای درج
    user_data = (
        "0xABC123Def456",     # wallet_address
        "satoshi_nakamoto",   # username
        "satoshi@example.com",# email
        "admin"               # role (admin/user/liquidity_provider/trader)
    )
    
    query = """
        INSERT INTO users (wallet_address, username, email, role)
        VALUES (?, ?, ?, ?)
    """
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(query, user_data)
        conn.commit()
        print("[✓] کاربر با موفقیت اضافه شد.")
        print(f"    آدرس کیف پول: {user_data[0]}")
    except sqlite3.IntegrityError as e:
        print("[!] خطا در درج: ", e)
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DATABASE_FILE):
        print("[!] فایل دیتابیس وجود ندارد. لطفاً ابتدا db_setup.py را اجرا کنید.")
    else:
        add_user()