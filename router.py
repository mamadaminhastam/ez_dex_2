# router.py
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from core import response, cookie, auth
import settings
import controllers.user_register
import controllers.user_login
import controllers.user_edit
import controllers.user_list
import controllers.pool_create
import controllers.pool_edit
import controllers.pool_list
import controllers.pool_delete
import controllers.contact_add
import controllers.contact_list
from core.navigation import get_nav_html


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def _handle(self, method):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b''
        data = parse_qs(body.decode('utf-8')) if body else {}

        # سرو فایل‌های استاتیک
        static_res = response.serve_static_file(path)
        if static_res:
            self._respond(*static_res)
            return

        result = self.route(path, method, data, query, self.headers)
        if result is not None:
            resp_body, resp_status, resp_headers = result
            self._respond(resp_body, resp_status, resp_headers)
        else:
            self._respond(*response._404())

    def _respond(self, body, status=200, headers=None):
        if headers is None:
            headers = {}
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            if isinstance(body, str):
                body = body.encode('utf-8')
            self.wfile.write(body)

    def route(self, path, method, data, query, headers):
        if path.startswith("/dex_1"):
            path = path[len("/dex_1"):] or "/"

        parts = path.strip("/").split("/")
        id = None
        if parts and parts[-1].isdigit():
            id = int(parts.pop())
            path = "/" + "/".join(parts)

        if method == "POST" and '_method' in data and data['_method']:
            method = data['_method'][0].upper()

        def add_nav(context):
            context["navigation"] = get_nav_html(headers)
            return context

        # ===================== GET =====================
        match (path, method):
            case ("/", "GET"):
                ctx = add_nav({"message": "Welcome to Ez Dex"})
                html = response.render_template("index.html", ctx)
                return response._200(html) if html else response._500()

            case ("/swap", "GET"):
                ctx = add_nav({})
                html = response.render_template("swap.html", ctx)
                return response._200(html) if html else response._500()

            case ("/register", "GET"):
                ctx = add_nav({"error": ""})
                html = response.render_template("register.html", ctx)
                return response._200(html) if html else response._500()

            case ("/login", "GET"):
                if auth.get_current_user(headers):
                    return response.redirect("/catalog")
                ctx = add_nav({"error": ""})
                html = response.render_template("login.html", ctx)
                return response._200(html) if html else response._500()

            case ("/logout", "GET"):
                headers_cookie = cookie.set_cookie(
                    'session_id', '', {"Max-Age": "0"})
                return response.redirect("/", headers_cookie)

            case ("/contact", "GET"):
                ctx = add_nav({"error": ""})
                html = response.render_template("contact.html", ctx)
                return response._200(html) if html else response._500()

            case ("/catalog", "GET"):
                pools = controllers.pool_list.handle(only_active=True)
                cards = ""
                for pool in pools:
                    active_badge = "Active" if pool['is_active'] else "Inactive"
                    cards += f"""<div style="background:var(--card-bg); border:1px solid var(--border); border-radius:var(--radius); padding:1.5rem;">
                        <h3>{pool['token0_symbol']}/{pool['token1_symbol']}</h3>
                        <p>Rate: {pool['initial_rate']}</p>
                        <p>Liquidity: {pool['initial_liquidity'] or 'N/A'}</p>
                        <span class="badge">{active_badge}</span>
                    </div>"""
                ctx = add_nav({"pool_cards": cards or "<p>No pools yet.</p>"})
                html = response.render_template("catalog.html", ctx)
                return response._200(html) if html else response._500()

            case ("/create_pool", "GET"):
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403("Only admins can create pools.") if auth.get_current_user(headers) else response._401()
                ctx = add_nav({"error": ""})
                html = response.render_template("create_pool.html", ctx)
                return response._200(html) if html else response._500()

            case ("/edit_pool", "GET") if id:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403("Admins only.") if auth.get_current_user(headers) else response._401()
                conn = __import__('core.db_utils', fromlist=[
                                  'get_db_connection']).get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM liquidity_pools WHERE id=? AND is_deleted=0", (id,))
                row = cur.fetchone()
                conn.close()
                if not row:
                    return response._404()
                pool = dict(row)
                active_sel = "selected" if pool['is_active'] else ""
                inactive_sel = "" if pool['is_active'] else "selected"
                ctx = add_nav({
                    "id": pool['id'], "token0_address": pool['token0_address'],
                    "token1_address": pool['token1_address'], "token0_symbol": pool['token0_symbol'] or '',
                    "token1_symbol": pool['token1_symbol'] or '', "initial_rate": pool['initial_rate'],
                    "initial_liquidity": pool['initial_liquidity'] or '', "is_active": str(pool['is_active']),
                    "active_selected": active_sel, "inactive_selected": inactive_sel, "error": ""
                })
                html = response.render_template("edit_pool.html", ctx)
                return response._200(html) if html else response._500()

            case ("/admin/users", "GET") if not id:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403("Admins only.") if auth.get_current_user(headers) else response._401()
                users = controllers.user_list.handle()
                rows = ""
                for u in users:
                    rows += f"<tr><td>{u['id']}</td><td>{u['username']}</td><td>{u['email']}</td><td>{u['role']}</td><td>{u['created_at']}</td><td><a href='/edit_user/{u['id']}'>Edit</a></td></tr>"
                ctx = add_nav(
                    {"user_rows": rows or "<tr><td colspan='6'>No data</td></tr>"})
                html = response.render_template("admin_users.html", ctx)
                return response._200(html) if html else response._500()

            case ("/edit_user", "GET") if id:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403("Admins only.") if auth.get_current_user(headers) else response._401()
                conn = __import__('core.db_utils', fromlist=[
                                  'get_db_connection']).get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE id=?", (id,))
                row = cur.fetchone()
                conn.close()
                if not row:
                    return response._404()
                u = dict(row)
                roles = ['user', 'liquidity_provider', 'trader', 'admin']
                role_options = ""
                for r in roles:
                    sel = "selected" if u['role'] == r else ""
                    role_options += f"<option value='{r}' {sel}>{r}</option>"
                ctx = add_nav({"id": u['id'], "username": u['username'],
                              "email": u['email'], "role_options": role_options, "error": ""})
                html = response.render_template("edit_user.html", ctx)
                return response._200(html) if html else response._500()

            # --- NEW: GET /admin/pools/<id> redirects to list ---
            case ("/admin/pools", "GET") if id:
                return response.redirect("/admin/pools")

            case ("/admin/pools", "GET") if not id:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403("Admins only.") if auth.get_current_user(headers) else response._401()
                pools = controllers.pool_list.handle(include_deleted=True)
                rows = ""
                for p in pools:
                    status_label = "<span style='color:green;'>Active</span>" if p['is_active'] and not p['is_deleted'] else (
                        "<span style='color:orange;'>Inactive</span>" if not p['is_deleted'] else "<span style='color:red;'>Deleted</span>")
                    if p['is_deleted']:
                        action_buttons = "<span style='color:#888;'>deleted</span>"
                    else:
                        action_buttons = f"<a href='/edit_pool/{p['id']}'>✏️ Edit</a> "
                        action_buttons += f"<form method='POST' action='/admin/pools/{p['id']}' style='display:inline;margin:0;padding:0;'>"
                        action_buttons += "<input type='hidden' name='_method' value='DELETE'>"
                        action_buttons += "<button type='submit' onclick=\"return confirm('Are you sure?')\">🗑️ Delete</button></form>"
                    rows += response.render_template("pool-table-row.html", {
                        "id": p['id'], "token0_symbol": p['token0_symbol'], "token1_symbol": p['token1_symbol'],
                        "initial_rate": p['initial_rate'], "initial_liquidity": p['initial_liquidity'],
                        "status_label": status_label, "action_buttons": action_buttons
                    })
                ctx = add_nav(
                    {"pool_rows": rows or "<tr><td colspan='7'>No data</td></tr>"})
                html = response.render_template("admin_pools.html", ctx)
                return response._200(html) if html else response._500()

            case ("/admin/messages", "GET") if not id:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403("Admins only.") if auth.get_current_user(headers) else response._401()
                messages = controllers.contact_list.handle()
                rows = ""
                for m in messages:
                    rows += f"<tr><td>{m['id']}</td><td>{m['email']}</td><td>{m['subject']}</td><td>{m['message']}</td><td>{m['created_at']}</td></tr>"
                ctx = add_nav(
                    {"message_rows": rows or "<tr><td colspan='5'>No data</td></tr>"})
                html = response.render_template("admin_messages.html", ctx)
                return response._200(html) if html else response._500()

        # ===================== POST =====================
        match (path, method):
            # --- Delete pool (placed early to avoid any shadowing, though path is unique) ---
            case ("/admin/pools", method) if id and method in ["POST", "DELETE"]:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403() if auth.get_current_user(headers) else response._401()
                success, msg = controllers.pool_delete.handle(id)
                if success:
                    return response.redirect("/admin/pools")
                return response._500()

            case ("/register", "POST"):
                success, msg = controllers.user_register.handle(data)
                if success:
                    return response.redirect("/login")
                ctx = add_nav({"error": msg})
                html = response.render_template("register.html", ctx)
                return response._200(html) if html else response._500()

            case ("/login", "POST"):
                user, session_or_msg = controllers.user_login.handle(data)
                if user:
                    headers = cookie.set_cookie('session_id', session_or_msg)
                    return response.redirect("/catalog", headers)
                ctx = add_nav({"error": session_or_msg})
                html = response.render_template("login.html", ctx)
                return response._200(html) if html else response._500()

            case ("/contact", "POST"):
                user = auth.get_current_user(headers)
                success, msg = controllers.contact_add.handle(
                    data, user['id'] if user else None)
                ctx = add_nav(
                    {"error": msg if not success else "Message sent."})
                html = response.render_template("contact.html", ctx)
                return response._200(html) if html else response._500()

            case ("/create_pool", "POST"):
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403() if auth.get_current_user(headers) else response._401()
                success, msg = controllers.pool_create.handle(data, user['id'])
                if success:
                    return response.redirect("/catalog")
                ctx = add_nav({"error": msg})
                html = response.render_template("create_pool.html", ctx)
                return response._200(html) if html else response._500()

            case ("/edit_pool", method) if id and method in ["POST", "PUT"]:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403() if auth.get_current_user(headers) else response._401()
                success, msg = controllers.pool_edit.handle(id, data)
                if success:
                    return response.redirect("/admin/pools")
                conn = __import__('core.db_utils', fromlist=[
                                  'get_db_connection']).get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM liquidity_pools WHERE id=? AND is_deleted=0", (id,))
                row = cur.fetchone()
                conn.close()
                if row:
                    pool = dict(row)
                    active_sel = "selected" if pool['is_active'] else ""
                    inactive_sel = "" if pool['is_active'] else "selected"
                    ctx = add_nav({
                        "id": pool['id'], "token0_address": pool['token0_address'],
                        "token1_address": pool['token1_address'], "token0_symbol": pool['token0_symbol'] or '',
                        "token1_symbol": pool['token1_symbol'] or '', "initial_rate": pool['initial_rate'],
                        "initial_liquidity": pool['initial_liquidity'] or '', "is_active": str(pool['is_active']),
                        "active_selected": active_sel, "inactive_selected": inactive_sel, "error": msg
                    })
                    html = response.render_template("edit_pool.html", ctx)
                    return response._200(html) if html else response._500()
                return response._404()

            case ("/edit_user", "POST") if id:
                user = auth.require_role(headers, ['admin'])
                if not user:
                    return response._403() if auth.get_current_user(headers) else response._401()
                success, msg = controllers.user_edit.handle(id, data)
                if success:
                    return response.redirect("/admin/users")
                conn = __import__('core.db_utils', fromlist=[
                                  'get_db_connection']).get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE id=?", (id,))
                row = cur.fetchone()
                conn.close()
                if row:
                    u = dict(row)
                    roles = ['user', 'liquidity_provider', 'trader', 'admin']
                    role_options = ""
                    for r in roles:
                        sel = "selected" if u['role'] == r else ""
                        role_options += f"<option value='{r}' {sel}>{r}</option>"
                    ctx = add_nav({"id": u['id'], "username": u['username'],
                                  "email": u['email'], "role_options": role_options, "error": msg})
                    html = response.render_template("edit_user.html", ctx)
                    return response._200(html) if html else response._500()
                return response._404()

            case _ if path.startswith("/static/"):
                static_res = response.serve_static_file(path)
                return static_res if static_res else response._404()

            case _:
                return None
