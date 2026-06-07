import json
from pathlib import Path
import importlib.util
import sqlite3

def run_db_setup():
    base_dir = Path(__file__).resolve().parent
    db_setup_path = base_dir / "db_setup.py"
    if not db_setup_path.exists():
        return "db_setup.py not found"
    spec = importlib.util.spec_from_file_location("project2_db_setup", db_setup_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "setup_database"):
        module.setup_database()
        return "Database setup completed"
    return "setup_database() not found in db_setup.py"

def render_template(filename):
    base_dir = Path(__file__).resolve().parent
    template_path = base_dir / "templates" / filename
    if not template_path.exists():
        return None
    return template_path.read_text(encoding="utf-8")

def get_all_products_html():
    db_path = Path(__file__).resolve().parent / "app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, description FROM products")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "<p>هیچ محصولی یافت نشد.</p>"
    cards = ""
    for name, price, description in rows:
        cards += f"""
        <article class="product-card">
            <h3 class="product-title">{name}</h3>
            <p class="product-price">{price:,} تومان</p>
            <p class="product-desc">{description}</p>
        </article>
        """
    return cards

def route(path, method, body):
    match path:
        case "/setup":
            result = run_db_setup()
            return (f"<p>{result}</p>", 200, {"Content-Type": "text/html; charset=utf-8"})

        case "/":
            html = render_template("index.html")
            if html:
                return (html, 200, {"Content-Type": "text/html; charset=utf-8"})
            return ("Template index.html not found", 500, {"Content-Type": "text/plain"})

        case "/contact":
            if method == "GET":
                html = render_template("contact.html")
                if html:
                    return (html, 200, {"Content-Type": "text/html; charset=utf-8"})
                return ("Template contact.html not found", 500, {"Content-Type": "text/plain"})
            elif method == "POST":
                base_dir = Path(__file__).resolve().parent
                module_path = base_dir / "add_message.py"
                if not module_path.exists():
                    return ("Controller add_message.py not found", 500)
                spec = importlib.util.spec_from_file_location("add_message_module", module_path)
                controller = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(controller)
                controller.handle(body)
                return ("<p>پیام شما با موفقیت ثبت شد</p>", 200, {"Content-Type": "text/html; charset=utf-8"})
            else:
                return ("Method Not Allowed", 405, {"Content-Type": "text/plain"})

        case "/about":
            html = render_template("about.html")
            if html:
                return (html, 200, {"Content-Type": "text/html; charset=utf-8"})
            return ("Template about.html not found", 500, {"Content-Type": "text/plain"})

        case "/api/status":
            data = {"project": "project2", "status": "ok"}
            return (json.dumps(data, ensure_ascii=False), 200, {"Content-Type": "application/json"})

        case "/product/all":
            if method != "GET":
                return ("Method Not Allowed", 405, {"Content-Type": "text/plain"})
            cards_html = get_all_products_html()
            html = render_template("catalog.html")
            if html is None:
                return ("Template catalog.html not found", 500, {"Content-Type": "text/plain"})
            html = html.replace("{{ product_cards }}", cards_html)
            return (html, 200, {"Content-Type": "text/html; charset=utf-8"})

        case _:
            return ("Not Found", 404, {"Content-Type": "text/plain; charset=utf-8"})