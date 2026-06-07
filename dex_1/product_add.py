# product_add.py
import sqlite3
import os

DATABASE_FILE = "dex.db"

def add_product():
    # اطلاعات نمونه برای درج استخر نقدینگی (محصول)
    product_data = (
        "0xTokenA",           # token0_address
        "0xTokenB",           # token1_address
        "ETH",                # token0_symbol
        "USDC",               # token1_symbol
        "1 ETH = 3000 USDC",  # initial_rate
        "10",                 # initial_liquidity (مقدار توکن اول)
        "0xABC123Def456",     # creator_wallet (باید از قبل در users وجود داشته باشد)
        1                     # is_active (1 فعال، 0 غیرفعال)
    )
    
    query = """
        INSERT INTO liquidity_pools 
        (token0_address, token1_address, token0_symbol, token1_symbol, 
         initial_rate, initial_liquidity, creator_wallet, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(query, product_data)
        conn.commit()
        print("[✓] استخر نقدینگی (محصول) با موفقیت اضافه شد.")
        print(f"    جفت ارز: {product_data[2]}/{product_data[3]} - نرخ: {product_data[4]}")
    except sqlite3.IntegrityError as e:
        print("[!] خطا: احتمالاً creator_wallet در جدول users وجود ندارد. لطفاً ابتدا user_add.py را اجرا کنید.")
        print("    جزئیات: ", e)
    except sqlite3.Error as e:
        print("[!] خطا در درج: ", e)
    finally:
        conn.close()

if __name__ == "__main__":
    if not os.path.exists(DATABASE_FILE):
        print("[!] فایل دیتابیس وجود ندارد. لطفاً ابتدا db_setup.py را اجرا کنید.")
    else:
        add_product()