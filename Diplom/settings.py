import os
from pathlib import Path
import variables

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '(j9^*l+nq1hzte8xm_4aq7s3yp#altwpiqe8tq#n*(##-j!cr='

DEBUG = True

ALLOWED_HOSTS = []


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

ROOT_URLCONF = 'Diplom.urls'

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

WSGI_APPLICATION = 'Diplom.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Hotel_db',
        'USER': 'maksim',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'Diplom.custom_password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'Diplom.custom_password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'Diplom.custom_password_validation.NotNumericPasswordValidator',
    },
    {
        'NAME': 'Diplom.custom_password_validation.MaximumLengthValidator',
    },
]



LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True



AUTH_USER_MODEL = 'Account.CustomUser'

# ----- SMTP -----
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = variables.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = variables.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
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
