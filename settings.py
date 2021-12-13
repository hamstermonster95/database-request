"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

#from cryptography.fernet import Fernet

#key = Fernet.generate_key()
#os.environ['KOMBU_FERNET_KEY'] = key

from pathlib import Path
import os
import sqlalchemy as sa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'rwcd&%tw(+eylgu(4rc$96ydy%2983lh72m7)7%bqaq%sp(z_-')

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = 'True'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['*']
#SECURE_SSL_REDIRECT = bool(int(os.environ.get('DJANGO_ENABLE_SSL', '1')))
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'getdb.apps.GetdbConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_globals.middleware.Global',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware']

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.                 # Or path to database file if using sqlite3.
        'USER': 'rpm_analyst',                      # Not used with sqlite3.
        'PASSWORD': '0223b547-57ac-47b4-8f23-340c24ad2986',                  # Not used with sqlite3.
        'HOST': 'rpm-postgres.postgres.database.azure.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'NAME': 'rpm_db_prod'                    # Set to empty string for default. Not used with sqlite3.
    }
}

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

from urllib.parse import urlparse



# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

WEB_CONCURRENCY=1



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

LOGIN_REDIRECT_URL = '/'

# Add to test email:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



CACHE_TTL = 60 * 60 * 100000000000000000000
#from setuptools import setup

#setup(
#    entry_points={
#        'kombu.serializers': [
#            'my_serializer = my_module.serializer:register_args'
#        ]
#    }
#)
# CELERY STUFF
#BROKER_URL = 'redis://localhost:6379'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'
#CELERY_ACCEPT_CONTENT = ['application/json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_TIMEZONE = 'Africa/Nairobi'

#CORS_REPLACE_HTTPS_REFERER      = False
#HOST_SCHEME                     = "http://"
#SECURE_PROXY_SSL_HEADER         = None
#SECURE_SSL_REDIRECT             = False
#SESSION_COOKIE_SECURE           = False
#CSRF_COOKIE_SECURE              = False
#SECURE_HSTS_SECONDS             = None
#SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
#SECURE_FRAME_DENY               = False



#CELERY_RESULT_BACKEND= 'django-db'
#CELERY_CACHE_BACKEND = 'django-cache'
#BROKER_URL = os.environ.get("REDISCLOUD_URL", "django://")
#BROKER_POOL_LIMIT = None
#from kombu_fernet.serializers.json import MIMETYPE

BROKER_URL = os.environ.get("redis://default:D3r05IHJjO2CSNi5L7RnPCCD8HhqN8Yh@redis-11512.c16.us-east-1-3.ec2.cloud.redislabs.com:11512","django://")

#redis_url = 'redis://default:D3r05IHJjO2CSNi5L7RnPCCD8HhqN8Yh@redis-11512.c16.us-east-1-3.ec2.cloud.redislabs.com:11512'
#BROKER_URL = redis.from_url(os.environ.get("REDIS_URL"))
CELERY_RESULT_BACKEND = "db+postgres://mcwawqifnzycxm:59e93cff9c7be4206f3d44592f9de5b464a8faa884c8d2cde30c9f7b5aaf7b91@ec2-52-71-153-228.compute-1.amazonaws.com:5432/d3k8qd4kpeu938"

CELERY_CACHE_BACKEND = 'django-cache'



CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



