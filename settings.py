# settings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_NAME = 'ezdex.db'
DB_PATH = BASE_DIR / DB_NAME

TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_URL_PREFIX = "/static/"
# settings.py

print(f"DEBUG: TEMPLATE_DIR = {TEMPLATE_DIR}")  # این خط را موقتاً اضافه کنید
