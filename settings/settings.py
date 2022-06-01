import os
from pathlib import Path

from settings import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '(j9^*l+nq1hzte8xm_4aq7s3yp#altwpiqe8tq#n*(##-j!cr='

DEBUG = True

ALLOWED_HOSTS = ['*']

# if DEBUG:
#     LOGGING = {
#         'disable_existing_loggers': False,
#         'version': 1,
#         'handlers': {
#             'console': {
#                 # logging handler that outputs log messages to terminal
#                 'class': 'logging.StreamHandler',
#                 'level': 'DEBUG',  # message level to be written to console
#             },
#         },
#         'loggers': {
#             'django.db.backends': {
#                 # this sets root level logger to log debug and higher level
#                 # logs to console. All other loggers inherit settings from
#                 # root level logger.
#                 'handlers': ['console'],
#                 'level': 'DEBUG',
#                 'propagate': False,  # this tells logger to send logging message
#                 # to its parent (will send if set to True)
#             },
#             'django.db': {
#                 # django also has database level logging
#             },
#         },
#     }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Account',

    'Room',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.DB_NAME,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASSWORD,
        'HOST': config.DB_HOST,
        'PORT': config.DB_PORT,

    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'settings.custom_password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'settings.custom_password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'settings.custom_password_validation.NotNumericPasswordValidator',
    },
    {
        'NAME': 'settings.custom_password_validation.MaximumLengthValidator',
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'Account.CustomUser'

# ----- SMTP -----
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
EMAIL_HOST = config.EMAIL_HOST
EMAIL_USE_TLS = config.EMAIL_USE_TLS
EMAIL_PORT = config.DB_PORT
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PASSWORD_RESET_TIMEOUT_DAYS = 2
ACCOUNT_ACTIVATION_DAYS = 2

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
