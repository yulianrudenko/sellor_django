import os
import dj_database_url
from pathlib import Path
from core.settings_dir.base import *

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'empty')
DEBUG = False
ALLOWED_HOSTS = [
    'sellor.herokuapp.com',
	'127.0.0.1',
	'localhost',
]
INSTALLED_APPS = [
    'cloudinary_storage',
    'cloudinary',
    *INSTALLED_APPS
]
CHANNEL_LAYERS = {
    'default': {
        'BACKEND':'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    }
}

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': 'dumbo.db.elephantsql.com',
#         'PORT': '5432',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_STORAGE_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_STORAGE_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CSRF_TRUSTED_ORIGINS = ['https://sellor.herokuapp.com', 'https://www.sellor.herokuapp.com']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FROM_USER = os.getenv('EMAIL_FROM_USER')
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = os.getenv('EMAIL_FROM_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_VALIDATION_API_KEY = os.getenv('EMAIL_VALIDATION_API_KEY')
