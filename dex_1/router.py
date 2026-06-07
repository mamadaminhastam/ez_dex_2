# dex_1/router.py
import json
import sqlite3
import settings  # ← همه تنظیمات از این ماژول می‌آید

# ------------------ توابع کمکی دیتابیس ------------------
def init_db():
    conn = sqlite3.connect(settings.DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            wallet_address TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
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
    conn.commit()
    conn.close()

def error_response(code, msg):
    return (json.dumps({"error": msg}, ensure_ascii=False), code,
            {"Content-Type": "application/json; charset=utf-8"})

def success_response(data):
    return (json.dumps(data, ensure_ascii=False), 200,
            {"Content-Type": "application/json; charset=utf-8"})

def serve_static_file(path):
    if "/static/" not in path:
        return None
    relative_path = path.split("/static/")[-1]
    file_path = settings.STATIC_DIR / relative_path
    if file_path.exists() and file_path.is_file():
        ext = file_path.suffix.lower()
        mime = {
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".html": "text/html; charset=utf-8"
        }.get(ext, "application/octet-stream")
        try:
            content = file_path.read_text(encoding="utf-8")
            return (content, 200, {"Content-Type": mime})
        except Exception as e:
            return (f"Error reading file: {e}", 500, {"Content-Type": "text/plain"})
    return None

# ------------------ تابع اصلی مسیریابی ------------------
def route(path, method, body):
    print(f"[ROUTER] {method} {path}")

    # حذف پیشوند پروژه (اگر وجود داشت)
    if path.startswith(settings.APP_PREFIX):
        path = path[len(settings.APP_PREFIX):]
        if not path:
            path = "/"

    # سرویس فایل‌های استاتیک (css, js)
    static_res = serve_static_file(path)
    if static_res:
        return static_res

    # ---------- صفحات GET ----------
    if method == "GET":
        if path == "/":
            html_path = settings.TEMPLATES_DIR / "index.html"
            if html_path.exists():
                return (html_path.read_text(encoding="utf-8"), 200,
                        {"Content-Type": "text/html; charset=utf-8"})
        elif path == "/contact":
            html_path = settings.TEMPLATES_DIR / "contact_us.html"
            if html_path.exists():
                return (html_path.read_text(encoding="utf-8"), 200,
                        {"Content-Type": "text/html; charset=utf-8"})
        elif path == "/register":
            html_path = settings.TEMPLATES_DIR / "register.html"
            if html_path.exists():
                return (html_path.read_text(encoding="utf-8"), 200,
                        {"Content-Type": "text/html; charset=utf-8"})
        elif path == "/create_pool":
            html_path = settings.TEMPLATES_DIR / "create_pool.html"
            if html_path.exists():
                return (html_path.read_text(encoding="utf-8"), 200,
                        {"Content-Type": "text/html; charset=utf-8"})
        
        # ========== اضافه شد: نمایش جداول مدیریتی ==========
        elif path == "/admin/users":
            conn = sqlite3.connect(settings.DATABASE_FILE)
            cur = conn.cursor()
            cur.execute("SELECT wallet_address, username, email, role, created_at FROM users ORDER BY created_at DESC")
            users = cur.fetchall()
            conn.close()
            
            html = """<!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <title>مدیریت کاربران</title>
                <link rel="stylesheet" href="/static/css/main.css">
                <style>
                    .data-table { width: 100%; border-collapse: collapse; margin: 20px 0; direction: rtl; }
                    .data-table th, .data-table td { border: 1px solid #ddd; padding: 10px; text-align: right; }
                    .data-table th { background-color: #2a2e3a; color: white; }
                    .back-link { display: inline-block; margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="dex-container">
                    <h2>📋 لیست کاربران</h2>
                    <table class="data-table">
                        <thead>
                            <tr><th>آدرس کیف پول</th><th>نام کاربری</th><th>ایمیل</th><th>نقش</th><th>تاریخ ثبت</th></tr>
                        </thead>
                        <tbody>
            """
            for row in users:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
            html += """
                        </tbody>
                    </table>
                    <br><a href="/dex_1/" class="back-link">🔙 بازگشت به خانه</a>
                </div>
            </body>
            </html>
            """
            return (html, 200, {"Content-Type": "text/html; charset=utf-8"})
        
        elif path == "/admin/messages":
            conn = sqlite3.connect(settings.DATABASE_FILE)
            cur = conn.cursor()
            cur.execute("SELECT id, email, subject, message, wallet_address, created_at FROM contact_messages ORDER BY created_at DESC")
            messages = cur.fetchall()
            conn.close()
            
            html = """<!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <title>مدیریت پیام‌ها</title>
                <link rel="stylesheet" href="/static/css/main.css">
                <style>
                    .data-table { width: 100%; border-collapse: collapse; margin: 20px 0; direction: rtl; }
                    .data-table th, .data-table td { border: 1px solid #ddd; padding: 10px; text-align: right; }
                    .data-table th { background-color: #2a2e3a; color: white; }
                    .message-cell { max-width: 300px; word-wrap: break-word; }
                </style>
            </head>
            <body>
                <div class="dex-container">
                    <h2>✉️ پیام‌های تماس</h2>
                    <table class="data-table">
                        <thead>
                            <tr><th>ID</th><th>ایمیل</th><th>موضوع</th><th>پیام</th><th>آدرس کیف پول</th><th>زمان</th></tr>
                        </thead>
                        <tbody>
            """
            for row in messages:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td class='message-cell'>{row[3]}</td><td>{row[4] or '-'}</td><td>{row[5]}</td></tr>"
            html += """
                        </tbody>
                    </table>
                    <br><a href="/dex_1/" class="back-link">🔙 بازگشت به خانه</a>
                </div>
            </body>
            </html>
            """
            return (html, 200, {"Content-Type": "text/html; charset=utf-8"})
        
        elif path == "/admin/pools":
            conn = sqlite3.connect(settings.DATABASE_FILE)
            cur = conn.cursor()
            cur.execute("SELECT id, token0_symbol, token1_symbol, initial_rate, initial_liquidity, creator_wallet, is_active, created_at FROM liquidity_pools ORDER BY created_at DESC")
            pools = cur.fetchall()
            conn.close()
            
            html = """<!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <title>مدیریت استخرهای نقدینگی</title>
                <link rel="stylesheet" href="/static/css/main.css">
                <style>
                    .data-table { width: 100%; border-collapse: collapse; margin: 20px 0; direction: rtl; }
                    .data-table th, .data-table td { border: 1px solid #ddd; padding: 10px; text-align: right; }
                    .data-table th { background-color: #2a2e3a; color: white; }
                </style>
            </head>
            <body>
                <div class="dex-container">
                    <h2>💧 استخرهای نقدینگی</h2>
                    <table class="data-table">
                        <thead>
                            <tr><th>ID</th><th>نماد توکن1</th><th>نماد توکن2</th><th>نرخ اولیه</th><th>نقدینگی اولیه</th><th>سازنده</th><th>وضعیت</th><th>زمان ایجاد</th></tr>
                        </thead>
                        <tbody>
            """
            for row in pools:
                status = "فعال" if row[6] == 1 else "غیرفعال"
                html += f"<tr><td>{row[0]}</td><td>{row[1] or '-'}</td><td>{row[2] or '-'}</td><td>{row[3]}</td><td>{row[4] or '-'}</td><td>{row[5]}</td><td>{status}</td><td>{row[7]}</td></tr>"
            html += """
                        </tbody>
                    </table>
                    <br><a href="/dex_1/" class="back-link">🔙 بازگشت به خانه</a>
                </div>
            </body>
            </html>
            """
            return (html, 200, {"Content-Type": "text/html; charset=utf-8"})
        # ========== پایان اضافه شد ==========

    # ---------- API های POST ----------
    if method == "POST":
        if path == "/api/register":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                return error_response(400, "JSON نامعتبر")

            wallet = data.get("wallet_address")
            wallet = wallet.strip() if wallet else ""
            username = data.get("username")
            username = username.strip() if username else ""
            email = data.get("email")
            email = email.strip() if email else ""
            role = data.get("role", "user")

            if not username or not email:
                return error_response(400, "نام کاربری و ایمیل الزامی است")

            if not wallet:
                wallet = None

            try:
                init_db()
                conn = sqlite3.connect(settings.DATABASE_FILE)
                cur = conn.cursor()
                cur.execute("SELECT username FROM users WHERE username = ?", (username,))
                if cur.fetchone():
                    conn.close()
                    return error_response(409, "این نام کاربری قبلاً گرفته شده است")
                if wallet:
                    cur.execute("SELECT wallet_address FROM users WHERE wallet_address = ?", (wallet,))
                    if cur.fetchone():
                        conn.close()
                        return error_response(409, "این کیف پول قبلاً ثبت‌نام کرده است")
                cur.execute(
                    "INSERT INTO users (wallet_address, username, email, role) VALUES (?,?,?,?)",
                    (wallet, username, email, role)
                )
                conn.commit()
                conn.close()
                return success_response({"status": "success", "message": "ثبت‌نام موفق"})
            except sqlite3.Error as e:
                return error_response(500, f"خطای دیتابیس: {str(e)}")

        elif path == "/api/contact":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                return error_response(400, "JSON نامعتبر")
            email = (data.get("Email") or "").strip()
            subject = (data.get("Subject") or "").strip()
            message = (data.get("Message") or "").strip()
            wallet = (data.get("Wallet_Address") or "").strip()
            if not email or not subject or not message:
                return error_response(400, "ایمیل، موضوع و پیام الزامی است")
            init_db()
            conn = sqlite3.connect(settings.DATABASE_FILE)
            conn.execute(
                "INSERT INTO contact_messages (email, subject, message, wallet_address) VALUES (?,?,?,?)",
                (email, subject, message, wallet if wallet else None)
            )
            conn.commit()
            conn.close()
            return success_response({"status": "success"})

        elif path == "/api/create_pool":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                return error_response(400, "JSON نامعتبر")
            wallet = (data.get("wallet_address") or "").strip()
            token0 = (data.get("token0") or "").strip()
            token1 = (data.get("token1") or "").strip()
            initial_rate = (data.get("initial_rate") or "").strip()
            if not wallet or not token0 or not token1 or not initial_rate:
                return error_response(400, "پارامترهای ضروری وارد نشده")
            init_db()
            conn = sqlite3.connect(settings.DATABASE_FILE)
            cur = conn.cursor()
            cur.execute("SELECT wallet_address FROM users WHERE wallet_address = ?", (wallet,))
            if not cur.fetchone():
                conn.close()
                return error_response(403, "کاربر یافت نشد")
            cur.execute('''INSERT INTO liquidity_pools 
                (token0_address, token1_address, token0_symbol, token1_symbol,
                 initial_rate, initial_liquidity, creator_wallet)
                VALUES (?,?,?,?,?,?,?)''',
                (token0, token1, data.get("symbol0"), data.get("symbol1"),
                 initial_rate, data.get("initial_liquidity"), wallet))
            conn.commit()
            conn.close()
            return success_response({"status": "success"})

    # اگر مسیر API بود ولی پیدا نشد
    if path.startswith("/api"):
        return error_response(404, f"API endpoint '{path}' یافت نشد")

    # صفحات دیگر
    return error_response(404, f"مسیر '{path}' یافت نشد")