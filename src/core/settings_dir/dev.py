from core import constants

from core.settings_dir.base import *
from core import constants

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sellor',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FROM_USER = constants.EMAIL_FROM_USER
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = constants.EMAIL_FROM_USER
EMAIL_HOST_PASSWORD = constants.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
EMAIL_PORT = 587