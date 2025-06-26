import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['webserver']

INSTALLED_APPS = [
    "django_bootstrap5",
]

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}