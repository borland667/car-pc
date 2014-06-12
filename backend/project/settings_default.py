# coding: utf-8
"""
Django settings for project project.

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
SECRET_KEY = 'n-zy#3won2&#uka-ckfp5^%k-k@3g%cv1+@5*50hemx$w55riy'

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

    'djangobower',
    'djsupervisor',
    # 'corsheaders',

    'core',
    'obd',
)

STATICFILES_FINDERS = (
    'djangobower.finders.BowerFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
BOWER_COMPONENTS_ROOT = BASE_DIR

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.XsSharing',
)
BOWER_INSTALLED_APPS = (
    'underscore',
    'bootstrap#3.1.1',
    'angular#1.2.16',
    'angular-animate#1.2.16',
    'angular-route#1.2.16',
    'angular-resource#1.2.16',
    'angular-sanitize#1.2.16',
    'angular-mocks#1.2.16',
    "angular-cookies#1.2.16",
    "AngularJS-Toaster#0.4.6",
    "font-awesome#4.0.3",
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'car_pc.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1:8001',
# )
# CORS_ALLOW_HEADERS = (
#     'x-requested-with',
#     'content-type',
#     'accept',
#     'origin',
#     'authorization',
#     'x-csrftoken',
# )
# CORS_ALLOW_CREDENTIALS = True

XS_SHARING_ALLOWED_ORIGINS = "http://127.0.0.1:8001"
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

VIDEO_PATH = os.path.join(BASE_DIR, 'video')

SYNC_PATH = '/home/car_pc/dropbox'
MUSIC_PATH = os.path.join(SYNC_PATH, 'music')

VLC_HTTP = 'http://127.0.0.1:8080'
VLC_LOGIN = ''
VLC_PASSWORD = '123'

OBD_DEV_PATH = '/dev/tty.SLAB_USBtoUART'