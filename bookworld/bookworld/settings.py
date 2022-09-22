"""
Django settings for bookworld project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from operator import truediv
from pathlib import Path
import os
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# sentry_sdk.init(
#     dsn=config("SENTRYDSN"),
#     # dsn="https://875b70345e164073ba379e96e5086cf7@o1420173.ingest.sentry.io/6765105",
#     integrations=[
#         DjangoIntegration(),
#     ],

#     # # Set traces_sample_rate to 1.0 to capture 100%
#     # # of transactions for performance monitoring.
#     # # We recommend adjusting this value in production.
#     # traces_sample_rate=1.0,

#     # # If you wish to associate users to errors (assuming you are using
#     # # django.contrib.auth) you may enable sending PII data.
#     # send_default_pii=True
# )




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
#Paypal
ACCOUNT_SID=config("account_sid") 
AUTH_TOKEN=config("auth_token")
SERVICE=config("service_sid")
#Razorpay
RAZOR_KEY_ID=config("key_id")
RAZOR_KEY_SECRET=config("key_secret")
OPENEXCHANGEKEY=config("openexchangekey")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mathfilters',
    'accounts',
    'admins',
    'store',
    'category',
    'carts',
    'orders',
    'salesreport',
    'notfoundhandler',
    'storages',
    
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

ROOT_URLCONF = 'bookworld.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'bookworld.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bookworld2',
        'USER': 'postgres',
        'PASSWORD':'arvi9895',
        'HOST':'awseb-e-c9dgzg6fru-stack-awsebrdsdatabase-5jlucff67da9.cth4om7nct5b.us-west-2.rds.amazonaws.com'
    }
}
#  'HOST':'awseb-e-c9dgzg6fru-stack-awsebrdsdatabase-5jlucff67da9.cth4om7nct5b.us-west-2.rds.amazonaws.com'
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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
# STATIC_ROOT  = os.path.join(BASE_DIR, 'staticfiles')

# AWS S3 Static Files Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    'static',
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'bookworld.media_storages.MediaStorage'



MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
