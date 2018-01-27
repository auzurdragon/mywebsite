"""
Django settings for mywebsite project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from mongoengine import connect

# 建立对数据库的连接
connect("mywebsite", host="localhost", port=28010)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4csj$_2@&0h08q!!(&x^1$j)se(*la03!xh0+w^o-v(+o(g!8e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['112.74.161.9', '192.168.1.108', 'localhost', 'www.5izan.site']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mywebsite',
    'examples',
    'mycms',                        # 管理后台
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

ROOT_URLCONF = 'mywebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [   # 指定模板加载路径
            'templates/',             # 绝对路径, <webroot>/templates
            'templates/mycase/',
            '/var/www/mywebsite/templates/',    # 服务器端的模板目录路径
	    '/var/www/mywebsite/templates/mycase/',
            os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/') # 相对路径,各应用模板路径的关键
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # 加载request
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mywebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# Django1.9以后language code 'zh-cn'就被丢弃了，使用'zh-hans'代替。坑你没商量啊。
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'CCT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 映射到静态文件的url
STATIC_URL = '/static/'

# 存放各个app的static和公共static目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    'static/',
    'mycms/static/',
]

# 设置生产环境的静态文件目录，使用python manage.py collectstatic可以把开发环境各个静态文件收集到该目录，交由http服务统一管理
STATIC_ROOT = "/var/www/mywebsite/collectstatic/"
