"""
Django settings for yund project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True  
# ALLOWED_HOSTS = []

# DEBUG = False
# ALLOWED_HOSTS = ['*'] 
ALLOWED_HOSTS = ['47.95.207.67','localhost','0.0.0.0:8000','127.0.0.1']

SECRET_KEY='asdfsdafsfsajlfksdlkfslsfs'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shops',
    'rest_framework',
    'crispy_forms',
    'mmadmin',
    'home',
    'service',   # 服务app
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

ROOT_URLCONF = 'yund.urls'

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

WSGI_APPLICATION = 'yund.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 新版drf schema_class默认用的是rest_framework.schemas.openapi.AutoSchema
    # "DEFAULT_AUTHENTICATION_CLASSES":['shops.auth.JwtQuertParamsAuthentication',]

}


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# 线上数据库
# DATABASES = {
#    'default': {
#           'ENGINE': 'django.db.backends.mysql', #数据库引擎
#           'NAME': 'mama_kaifa_zgydg',                       #数据库名
#           'USER': 'mama_kaifa_zgydg',                       #用户名
#           'PASSWORD': 'SP2xfaTwfACEy4mK',                   #密码
#           'HOST': '47.113.194.115',                           #数据库主机，默认为localhost
#           'PORT': '',                           #数据库端口，MySQL默认为3306
#           'OPTIONS': {
#              'autocommit': True,
#          }
#     }
# }

# 本地数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mama_kaifa',    # 你的数据库名称
        'USER': 'root',   #你的数据库用户名
        'PASSWORD': '', #你的数据库密码
        'HOST': 'localhost', #你的数据库主机，留空默认为localhost
        'PORT': '3306', #你的数据库端口
    }}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

UPLOAD_ROOT = os.path.join(BASE_DIR,'upload')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


# 短信账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 登录用户中心->验证码短信->产品总览->APIID
APIID = "C01362267"
# 登录用户中心->验证码短信->产品总览->APIKEY
APIKEY = "fc638bf958f35e28994ebb99d2a5f45a"

# URL = "http://127.0.0.1:8000/"
URL = "0.0.0.0:8000/"



# 发短信
host="106.ihuyi.com"
sms_send_uri="/webservice/sms.php?method=Submit"