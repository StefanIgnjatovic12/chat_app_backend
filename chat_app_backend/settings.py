"""
Django settings for chat_app_backend project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

import boto3
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--m82r=436id=+l6&#+3p45rtu$1r5*7i)(vy0=sy0p=@1!$(kz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['drf-react-chat-backend.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',
    'dj_rest_auth',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'chat_app_backend.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'chat_app_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# old working version
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = 'static/'
# # MEDIA_ROOT = 'C:/Users/Stefan/Desktop/python/chat_app_backend/avatars/'
# MEDIA_ROOT = 'C:/Users/Stefan/Desktop/python/chat_app_backend/'
# MEDIA_URL = ('avatars/')

# STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected-static'

# MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'collected-media'

# The following configs determine if files get served from the server or an S3 storage
S3_ENABLED = config('S3_ENABLED', cast=bool, default=False)
# LOCAL_SERVE_MEDIA_FILES = config('LOCAL_SERVE_MEDIA_FILES', cast=bool, default=not S3_ENABLED)
# LOCAL_SERVE_STATIC_FILES = config('LOCAL_SERVE_STATIC_FILES', cast=bool, default=not S3_ENABLED)
#
# if (not LOCAL_SERVE_MEDIA_FILES or not LOCAL_SERVE_STATIC_FILES) and not S3_ENABLED:
#     raise ValueError('S3_ENABLED must be true if either media or static files are not served locally')

# if S3_ENABLED:
AWS_ACCESS_KEY_ID = config('BUCKETEER_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('BUCKETEER_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('BUCKETEER_BUCKET_NAME')
AWS_S3_REGION_NAME = config('BUCKETEER_AWS_REGION')
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = config('S3_SIGNATURE_VERSION', default='s3v4')
AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}


STATIC_DEFAULT_ACL = 'public-read'
STATIC_LOCATION = 'static'
STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'utils.storage_backends.StaticStorage'

PUBLIC_MEDIA_DEFAULT_ACL = 'public-read'
PUBLIC_MEDIA_LOCATION = 'media/public'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'utils.storage_backends.PublicMediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )

}
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'chat-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# JWT
from datetime import timedelta
from django.conf import settings

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=10),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=20),
}

ACCOUNT_EMAIL_VERIFICATION = "none"
