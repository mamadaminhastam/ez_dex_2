# message_add.py
import sqlite3
import os

DATABASE_FILE = "dex.db"

def add_message():
    # اطلاعات نمونه برای درج پیام
    message_data = (
        "user@example.com",           # email
        "مشکل در اتصال کیف پول",       # subject
        "سلام، من نمی‌توانم کیف پول خود را به صرافی متصل کنم. لطفاً راهنمایی کنید.",  # message
        "0xABC123Def456"              # wallet_address (اختیاری، می‌تواند None باشد)
    )
    
    query = """
        INSERT INTO contact_messages (email, subject, message, wallet_address)
        VALUES (?, ?, ?, ?)
    """
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(query, message_data)
        conn.commit()
        print("[✓] پیام با موفقیت اضافه شد.")
        print(f"    موضوع: {message_data[1]}")
    except sqlite3.Error as e:
        print("[!] خطا در درج: ", e)
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DATABASE_FILE):
        print("[!] فایل دیتابیس وجود ندارد. لطفاً ابتدا db_setup.py را اجرا کنید.")
    else:
        add_message()