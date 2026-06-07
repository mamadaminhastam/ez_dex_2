# web_server.py (همان فایل قبلی اصلاح شده)
import json
import os
import sys
import importlib.util
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECTS = {}

def load_router(module_path):
    spec = importlib.util.spec_from_file_location("router_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def auto_load_projects():
    print("Scanning for projects...")
    for item in BASE_DIR.iterdir():
        if not item.is_dir():
            continue
        if item.name in ["__pycache__", "venv"]:
            continue
        router_file = item / "router.py"
        if not router_file.exists():
            continue
        project_name = item.name
        print(f"Found project: {project_name}")
        try:
            sys.path.insert(0, str(item))
            module = load_router(router_file)
        except Exception as e:
            print(f"ERROR loading router for {project_name}: {e}")
            continue
        if not hasattr(module, "route"):
            print(f"WARNING: {project_name}/router.py missing 'route' function")
            continue
        PROJECTS[project_name] = module
        print(f"[OK] Project '{project_name}' loaded.")

class MultiProjectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request("GET")
    def do_POST(self):
        self.handle_request("POST")
    def handle_request(self, method):
        parsed = urlparse(self.path)
        path = parsed.path
        parts = path.strip("/").split("/")
        if not parts or parts == ['']:
            return self.show_home()
        project = parts[0]
        if project not in PROJECTS:
            return self.send_not_found(f"Project '{project}' not found.")
        inner_path = "/" + "/".join(parts[1:]) if len(parts) > 1 else "/"
        body = None
        if method == "POST":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else ""
        try:
            response_text, status, headers = PROJECTS[project].route(
                inner_path, method, body
            )
            self.send_response(status)
            for h, v in headers.items():
                self.send_header(h, v)
            self.end_headers()
            self.wfile.write(response_text.encode("utf-8"))
        except Exception as e:
            if inner_path.startswith("/api"):
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Router error: {e}"}).encode())
            else:
                self.send_not_found(f"Router error: {e}")
    def show_home(self):
        html = "<h1>Multi-Project Server</h1><ul>"
        for name in PROJECTS.keys():
            html += f"<li><a href='/{name}'>{name}</a></li>"
        html += "</ul>"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
    def send_not_found(self, msg="Not found"):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(msg.encode("utf-8"))

def run_server():
    auto_load_projects()
    print("Server running on http://localhost:8000 ...")
    server = HTTPServer(("0.0.0.0", 8000), MultiProjectHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()