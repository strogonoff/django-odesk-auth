"""
Django settings for example project for django-odesk-auth application.
See settings that you have to fill in the end of file.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$ob8eqhrb-x^_ww!g**auezr01#4dz@_d-(e(@5^&&bx!gahka'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_odesk_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django_odesk_auth.backends.ODeskOAuthBackend',
)

ROOT_URLCONF = 'example_project.urls'

WSGI_APPLICATION = 'example_project.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 1


# Provide these settings to make test project work

# ODESK_OAUTH_KEY = ''
# ODESK_OAUTH_SECRET = ''
# 
# ODESK_AUTH_ALLOWED_USERS = (
#     '<your_username>@odesk.com'
# )

ODESK_OAUTH_KEY = '8e7cc6872e54bfa8b2220f1386f37ff1'
ODESK_OAUTH_SECRET = '8702f61f892b92e7'

ODESK_AUTH_ALLOWED_USERS = (
    'astrogov@odesk.com'
)
ODESK_AUTH_ALLOWED_TEAMS = ()
ODESK_AUTH_ADMINS = ()
ODESK_AUTH_ADMIN_TEAMS = ()
ODESK_AUTH_SUPERUSERS = ()
ODESK_AUTH_SUPERUSER_TEAMS = ()

ODESK_AUTH_CREATE_UNKNOWN_USER = True
