"""production specific django settings"""

import os
from django.core.exceptions import ImproperlyConfigured
from .settings import BASE_DIR


# key and debugging settings should not changed without care
SECRET_KEY = os.getenv("SECRET_KEY") or ImproperlyConfigured("SECRET_KEY not set")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# allowed hosts get parsed from a comma-separated list
hosts = os.getenv("HOSTS") or ImproperlyConfigured("HOSTS not set")
hosts = os.getenv("ALLOWED_HOSTS", "")  # Provide an empty string as a default
if not hosts:
    raise ImproperlyConfigured("ALLOWED_HOSTS environment variable is not set")
ALLOWED_HOSTS = hosts.split(",")

cors_allowed_oigins = os.getenv("CORS_ALLOWED_ORIGINS") or ImproperlyConfigured(
    "CORS_ALLOWED_ORIGINS not set"
)

try:
    CORS_ALLOWED_ORIGINS = cors_allowed_oigins.split(",")
except:
    raise ImproperlyConfigured("CORS_ALLOWED_ORIGINS could not be parsed")


# Database
if os.getenv("USESQLITE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    name = os.getenv("DB_NAME") or ImproperlyConfigured("DB_NAME not set")
    user = os.getenv("DB_USER") or ImproperlyConfigured("DB_USER not set")
    password = os.getenv("DB_PASSWORD") or ImproperlyConfigured(
        "DB_PASSWORD not set"
    )
    host = os.getenv("DB_HOST") or ImproperlyConfigured("DB_HOST not set")
    port = os.getenv("DB_PORT") or ImproperlyConfigured("DB_PORT not set")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
    }

TIME_ZONE = "Asia/Karachi"

USE_TZ = False

# Static Files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# User uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# S3 Storage
s3_access_key_id = os.getenv("S3_ACCESS_KEY_ID") or ImproperlyConfigured(
    "S3_ACCESS_KEY_ID not set"
)
s3_secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY") or ImproperlyConfigured(
    "S3_SECRET_ACCESS_KEY not set"
)
s3_bucket_name = os.getenv("S3_BUCKET_NAME") or ImproperlyConfigured(
    "S3_BUCKET_NAME not set"
)
s3_region_name = os.getenv("S3_REGION_NAME") or ImproperlyConfigured(
    "S3_REGION_NAME not set"
)
s3_endpoint_url = os.getenv("S3_ENDPOINT_URL") or ImproperlyConfigured(
    "S3_ENDPOINT_URL not set"
)
s3_public_url = os.getenv("S3_PUBLIC_URL") or ImproperlyConfigured(
    "S3_PUBLIC_URL not set"
)

AWS_ACCESS_KEY_ID = s3_access_key_id
AWS_SECRET_ACCESS_KEY = s3_secret_access_key
AWS_STORAGE_BUCKET_NAME = s3_bucket_name
AWS_S3_REGION_NAME = s3_region_name
AWS_S3_ENDPOINT_URL = s3_endpoint_url
AWS_S3_PUBLIC_URL = s3_public_url

# STATIC_URL = f'{AWS_S3_PUBLIC_URL}/static/'
MEDIA_URL = f"{AWS_S3_PUBLIC_URL}/media/"
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
