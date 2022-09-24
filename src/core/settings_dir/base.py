import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

DEBUG = False
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'random_django_secret_key'
INTERNAL_IPS = ['127.0.0.1', 'localhost']
INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    # external packages/modules
    'rest_framework',
    'channels',
    # internal apps
    'core.apps.products',
    'core.apps.users',
    'core.apps.chats',
    'core.apps.search',
    'api'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.apps.products.context_processors.categories',
            ],
        },
    },
]
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

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
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Internationalization
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('pl', _('Polish')),
)
MODELTRANSLATION_LANGUAGES = ('en', 'pl')
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'
LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

STATIC_URL = '/static/'
FIXTURE_DIRS = [BASE_DIR / 'fixtures']

AUTH_USER_MODEL = 'users.UserAccount'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = "/"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}