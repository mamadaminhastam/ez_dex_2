# dex_1/settings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "dex.db"
TEMPLATES_DIR = BASE_DIR / "front_end" / "template" / "html"
STATIC_DIR = BASE_DIR / "front_end" / "static"

APP_PREFIX = "/dex_1"