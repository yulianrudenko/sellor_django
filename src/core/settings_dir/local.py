from core.settings_dir.base import *

DEBUG = True

ALLOWED_HOSTS = [
	'127.0.0.1',
	'localhost',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432
    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FROM_USER =  os.environ.get('EMAIL_FROM_USER')
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER =  os.environ.get('EMAIL_FROM_USER')
EMAIL_HOST_PASSWORD =  os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587