from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-production-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Domain configuration
DOMAIN = 'examples.whatznot.com'
ALLOWED_HOSTS = [DOMAIN, f'www.{DOMAIN}']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email configuration for cPanel
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.whatznot.com'  # Your cPanel mail server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = f'noreply@{DOMAIN}'
EMAIL_HOST_PASSWORD = 'your-email-password'  # Set this during deployment
DEFAULT_FROM_EMAIL = f'Examples <noreply@{DOMAIN}>'

# Admin configuration
ADMIN_URL = 'admin/'  # Change this to something unique during deployment
JAZZMIN_SETTINGS["site_title"] = "Examples Admin"
JAZZMIN_SETTINGS["site_header"] = "Examples"
JAZZMIN_SETTINGS["site_brand"] = "Examples Admin"
JAZZMIN_SETTINGS["welcome_sign"] = "Welcome to Examples Admin Panel"
JAZZMIN_SETTINGS["copyright"] = f"Examples @ {DOMAIN}"

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{name}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/error.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache',
    }
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_NAME = 'examples_sessionid'
SESSION_COOKIE_DOMAIN = DOMAIN
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# CSRF settings
CSRF_COOKIE_NAME = 'examples_csrftoken'
CSRF_COOKIE_DOMAIN = DOMAIN
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = [f'https://{DOMAIN}', f'https://www.{DOMAIN}']

# Compression settings for uploaded images
COMPRESS_IMAGES = True
COMPRESS_QUALITY = 60  # 60% quality for uploaded images 