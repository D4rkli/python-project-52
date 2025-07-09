import dj_database_url
from pathlib import Path

import rollbar
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    "webserver",
    "python-project-52-l36d.onrender.com"
]

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task_manager',
    'task_manager.tasks',
    'django_bootstrap5',
    'django_filters',
]

ROOT_URLCONF = 'task_manager.urls'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

LOGIN_URL = '/login/'


ROLLBAR = {
    'access_token': os.getenv('ROLLBAR_TOKEN'),
    'environment': 'production' if not DEBUG else 'development',
    'root': BASE_DIR,
}

if not DEBUG:
    rollbar.init(
        ROLLBAR['access_token'],
        ROLLBAR['environment'],
        root=ROLLBAR['root'],
    )

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'