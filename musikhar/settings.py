"""
Django settings for musikhar project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!kb!fbs77#30kwu-2m23_7m6cnd8-$z(&&ag&du@05@vi+cm+)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'opbeat.contrib.django',
    'rest_framework',
    'loginapp',
    'karaoke',
    'analytics',
    'mediafiles',
    'financial',
    'silk'
]

MIDDLEWARE = [
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'loginapp.middleware.AuthenticationMiddleware',
    'musikhar.middlewares.DomainMiddleware',
    'musikhar.middlewares.CatchTheException',
]

ROOT_URLCONF = 'musikhar.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/',
                 os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
                 ],
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

WSGI_APPLICATION = 'musikhar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'image'))

AUTH_USER_MODEL = 'loginapp.User'

AUTHENTICATION_BACKENDS = (
    'loginapp.auth.AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

OPBEAT = {
    'ORGANIZATION_ID': 'c3eb3a03ffc94916acca0329c2db5cbe',
    'APP_ID': 'b6b0bef243',
    'SECRET_TOKEN': '2c878bbd8c1bbb38a1d528e33c0ee70d3f821851',
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'std': {
            'format': '%(name)s [%(levelname)s] %(asctime)s - %(message)s'
        }
    },
    'handlers': {
        'application': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.environ.get('TZ_LOG_DIR', BASE_DIR), 'application.log')
        },
        'error': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.environ.get('TZ_LOG_DIR', BASE_DIR), 'errors.log')
        },
    },
    'loggers': {
        'application': {
            'handlers': ['application'],
            'level': 'INFO'
        },
        'error': {
            'handlers': ['error'],
            'level': 'INFO'
        }
    }

}


SYSTEM_USER = {
    'username': 'Canto',
    'email': 'Canto@canto-app.ir',
    'first_name': 'Canto',
    'password': 'NHgZGlyBaEQg5HEhjMuv'
}


APP_VERSION = {
    'android': {
        'min': 1,
        'max': 4
    },
    'ios': {
        'min': 1,
        'max': 4
    }
}

SILKY_AUTHORISATION = True
SILKY_PYTHON_PROFILER = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
KAVEHNEGAR_API = '755A75304B73387A6935775A4633793455754D3847673D3D'
