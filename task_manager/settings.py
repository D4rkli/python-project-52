import dj_database_url
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

ALLOWED_HOSTS = ["webserver"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
