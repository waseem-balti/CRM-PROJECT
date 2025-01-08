"""local runserver settings"""

import os

from .settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-drfy92((+yt#hp_#vp*uo7b21-vq4@$y*xhkt2g2n8e5#*vt!v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

TIME_ZONE = "Asia/Karachi"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:9000",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
# User uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
