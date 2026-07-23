from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = 'ezdex.db'
DB_PATH = BASE_DIR / DB_NAME              # مسیر مطلق: .../dex_1/ezdex.db
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
STATIC_URL_PREFIX = "/static/"
BASE_URL = "/dex_1"
