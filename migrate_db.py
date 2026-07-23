# migrate_db.py
import sqlite3

conn = sqlite3.connect('ezdex.db')
try:
    conn.execute(
        "ALTER TABLE liquidity_pools ADD COLUMN is_deleted INTEGER DEFAULT 0")
    conn.commit()
    print("✅ ستون is_deleted اضافه شد.")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e):
        print("ستون is_deleted از قبل وجود دارد.")
    else:
        print(f"خطا: {e}")
finally:
    conn.close()
