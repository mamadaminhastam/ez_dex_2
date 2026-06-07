# seed_products.py
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "app.db"


def seed():
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    # چند محصول نمونه
    products = [
        ("مداد", 15000, "مداد مشکی HB با پاک‌کن"),
        ("خودکار", 25000, "خودکار آبی روان‌نویس"),
        ("دفتر", 40000, "دفتر ۱۰۰ برگ سیمی"),
    ]
    cur.executemany(
        "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
        products
    )
    conn.commit()
    conn.close()
    print("محصولات نمونه اضافه شدند.")


if __name__ == "__main__":
    seed()
