from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    # 'rest_framework_simplejwt',
    "rest_framework_simplejwt.token_blacklist",
    'rest_framework',
    # 'rest_framework.authtoken',
    'drf_spectacular',
    'crmapp',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Ensure this is included
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'CRM_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'CRM_project.wsgi.application'



SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    'BLACKLIST_ENABLED': True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
USE_TZ = False


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/min',  # Anonymous users: 10 requests per minute
        'user': '1000/day',  # Authenticated users: 1000 requests per day
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'CRM API',
    'DESCRIPTION': 'Django CRM Team',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  
    'ENUM_NAME_OVERRIDES': {
        'industry': 'IndustryChoiceEnum',
        'client_budget': 'ClientBudgetEnum',
    },
    'SCHEMA_PATH_PREFIX': '/api/',
}

CORS_ALLOW_ALL_ORIGINS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'crmapp.CustomUser'


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
# EMAIL_USE_TLS = True

# EMAIL_USE_LOCALTIME = True
# EMAIL_DEBUG = True

if os.getenv("LOCAL") == "True":
    from .settings_dev import *
else:
    from .settings_prd import *


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }
