"""
Django scommon settings for polls project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import pathlib

base_dir = pathlib.Path(__file__).absolute().parents[2]
BASE_DIR = str(base_dir)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hmxabo(_0=fl$huk$qr#zkkp_m%%3opyqxzm%s$e(2*7vb62=g'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'bootstrap3',

    # Project apps
    'apps.polls.apps.PollsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware'
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(base_dir / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Custom processors
                'project.context_processors.settings_values'
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(base_dir / 'var' / 'db' / 'db.sqlite3')
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(base_dir / 'static')
]
STATIC_ROOT = str(base_dir / 'var' / 'static')

# bootstrap3
# ------------

# https://django-bootstrap3.readthedocs.io/en/latest/settings.html
BOOTSTRAP3 = {}

# Project settings
# ----------------

# Your public hostname or public IP address
MY_HOSTNAME_OR_IP = None


def _fix_my_hostname_or_ip():
    global MY_HOSTNAME_OR_IP
    if MY_HOSTNAME_OR_IP is None:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            MY_HOSTNAME_OR_IP = s.getsockname()[0]
    return


_fix_my_hostname_or_ip()

MY_WAMP_URL = 'ws://{}:8080/ws'.format(MY_HOSTNAME_OR_IP)
MY_WAMP_REALM = 'polls'
MY_WAMP_HTTP_GATEWAY = 'http://{}:8080/publish'.format(MY_HOSTNAME_OR_IP)
