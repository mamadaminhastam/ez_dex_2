import sqlite3
import hashlib

conn = sqlite3.connect('ezdex.db')
cur = conn.cursor()
password_hash = hashlib.sha256("admin123".encode()).hexdigest()
try:
    cur.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, 'admin')",
                ("admin", "admin@ezdex.com", password_hash))
    conn.commit()
    print("Admin user created (admin / admin123)")
except sqlite3.IntegrityError:
    print("Admin user already exists.")
finally:
    conn.close()
