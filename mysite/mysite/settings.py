"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wa%9h_z#d92c0dh)*t=a+cn!04pis^-f1zvo3lkm^r-s!u#s0t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.164.15','192.168.164.129','192.168.164.132']



BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Application definition

#from django.db import models
#FIELD_HISTORY_OBJECT_ID_TYPE = (models.CharField, {'max_length': 100})

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'reversion',
    'rest_framework',
    #'simple_history',

    #'field_history',
    #'django_celery_beat',
#    'djcelery',
#    'kombu.transport.django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'simple_history.middleware.HistoryRequestMiddleware',
    #'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'mysite1',
        'USER':'root',
        'PASSWORD':'abc123!@#',
        'HOST':'172.31.50.30',
        'PORT':'3306',
        'OPTION':{
            'init_command': "SET default_storage_engine=INNODB;SET sql_mode='STRICT_TRANS_TABLES'",

        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
DEFAULT_FILE_STORAGE = '/test/'
FILE_UPLOAD_PERMISSIONS= 0o600
MEDIA_ROOT='/home/yrenyi/temp/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

from datetime import timedelta
# sendemail2.delay()

CELERYBEAT_SCHEDULE = {
    # 'send-email-every-5-seconds': {
    #     'task': 'polls.tasks.sendEmailList',
    #     'schedule': timedelta(seconds=5),
    #     # 'args': ('你好','你好','dop1@ims.cn',['dop6@ims.cn'],['dop6@ims.cn'])
    #     'args':()
    # },
    # 'send-ip-every-5-seconds': {
    #         'task': 'polls.tasks.sendIpAddress',
    #         'schedule': timedelta(seconds=60),
    #         # 'args': ('你好','你好','dop1@ims.cn',['dop6@ims.cn'],['dop6@ims.cn'])
    #         'args':()
    #     },
}
