"""
Django settings for the TheBestCryptoCourse project.

Local dev: just run it, nothing extra needed -- SQLite is used automatically.
Production (Railway): set the environment variables below in Railway's
dashboard (Variables tab). Railway auto-provides DATABASE_URL when you
attach a Postgres database -- you don't need to build that URL yourself.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Core settings -- controlled by environment variables in production.
# Locally, sensible defaults are used automatically so you can just run it.
# ---------------------------------------------------------------------------

# SECRET_KEY = os.environ.get(
#     "SECRET_KEY",
#     "django-insecure-dev-only-key-change-this-in-production",
# )

SECRET_KEY = '1tuzlj*^b5&+3+h73auw2-*e8fz3sw33tj&z8#&h=t5$*)y=_j'
# DEBUG is True locally by default. On Railway, set DEBUG=False as an
# environment variable -- never leave debug mode on in production.
# DEBUG = os.environ.getS("DEBUG", "True") == "True"
DEBUG = True

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ALLOWED_HOSTS = ['*']

# Site display name -- shown in the header and page titles.
# Change this in one place instead of hunting through templates.
# SITE_NAME = os.environ.get("SITE_NAME", "TheBestCryptoCourse")
SITE_NAME = 'TheBestCryptoCourse'

# Where users are told to email their payment proof after sending crypto.
# Change this via the PAYMENT_CONFIRMATION_EMAIL environment variable in
# production -- no code change needed.
# PAYMENT_CONFIRMATION_EMAIL = os.environ.get("PAYMENT_CONFIRMATION_EMAIL", "payments@thebestcryptocourse.com")
PAYMENT_CONFIRMATION_EMAIL = "davidomisakin4good@gmail.com"

# Where Django sends people who need to log in, and where it sends them after
# logging in / out.
LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'core',
    'blog',
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # project-wide templates (base.html)
        'APP_DIRS': True,                  # each app's own templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',  # makes SITE_NAME available in every template
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ---------------------------------------------------------------------------
# Database
# Locally: SQLite (a single file, zero setup).
# Production: reads DATABASE_URL, which Railway sets automatically once you
# attach a Postgres database to this service.
# ---------------------------------------------------------------------------

# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
#         conn_max_age=600,
#     )
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_DIRS = [BASE_DIR / 'static']       # your source CSS/JS/images
STATIC_ROOT = BASE_DIR / 'staticfiles'          # collected here on deploy
# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
