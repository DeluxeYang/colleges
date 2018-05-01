"""
Django settings for college project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*1mc^52z@38=2vcyxt+m7@(4x86*co^k@=m8cw_61x#r_r@d+v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'basic',
    'backend',
    'api',
    'django_cleanup',
    'DjangoUeditor',
    'rest_framework',
)

MIDDLEWARE = [
    'basic.middleware.test.Test1',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'basic.middleware.dispatcher.QtsAuthentication'
]

ROOT_URLCONF = 'college.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'college.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'college',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',  # os.environ['MYSQL_PORT_3306_TCP_ADDR'],
        'PORT': '5432',
    },
    # 'mysql': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'college',
    #     'USER': 'root',
    #     'PASSWORD': '123456',
    #     'HOST': 'localhost',  # os.environ['MYSQL_PORT_3306_TCP_ADDR'],
    #     'PORT': '3306',
    # }
}

# ElasticSearch
es_address = [{'host': '127.0.0.1', 'port': 9200}]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
# 数据库永远存储UTC，但显示时永远显示本地
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 收集admin的static时使用
STATICFILES_DIRS = [  # Debug开发时的静态文件处理
    os.path.join(BASE_DIR, 'static')
]

LOGIN_URL = '/login/'

MEDIA_ROOT = 'upload/'

MEDIA_URL = '/upload/'
# celery
BROKER_URL = 'redis://127.0.0.1:6379/0'

CELERY_TIMEZONE = TIME_ZONE

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 50
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'json': {
            'format': '{"level": "%(levelname)s", "time": "%(asctime)s", '
                      '"function": "%(module)s:%(funcName)s", "line_number": "%(lineno)d", '
                      '"message": "%(message)s"}'
        },
        'standard': {
            'format': '%(asctime)s [%(module)s:%(funcName)s][%(lineno)d]'
                      '[%(levelname)s]- %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/all.log',     # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,                  # 文件大小
            'backupCount': 5,                         # 备份份数
            'formatter': 'json',                   # 使用哪种formatters日志格式
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/request.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'college': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
