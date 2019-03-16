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

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.148', '192.168.1.114', '192.168.0.193', '192.168.1.49']

REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'opbeat.contrib.django',
    'ddtrace.contrib.django',
    'django_elasticsearch_dsl',
    'rest_framework',
    'loginapp',
    'karaoke',
    'analytics',
    'mediafiles',
    'financial',
    'inventory',
    # 'silk',
    'rangefilter',
    'constance'
]

MIDDLEWARE = [
    # 'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'loginapp.middleware.ExpiredVersionMiddleware',
    'loginapp.middleware.AuthenticationMiddleware',
    'musikhar.middlewares.DomainMiddleware',
    'musikhar.middlewares.CatchTheException',
    'musikhar.middlewares.VersionMiddleWare'
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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'canto_local',
        'USER': 'canto',
        'PASSWORD': 'canto6524',
        'HOST': 'localhost',
        'PORT': '',
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
    'DEFAULT_PAGINATION_CLASS': 'musikhar.abstractions.pagination.DescriptedPagination',
    'PAGE_SIZE': 30
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
        'celery': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.environ.get('TZ_LOG_DIR', BASE_DIR), 'celery.log')
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
        },
        'celery': {
            'handlers': ['celery'],
            'level': 'INFO'
        },
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
        'max': 6
    }
}

DOWNLOAD_LINKS = {
    'android': 'http://yahoo.com',
    'ios': {'url': 'http://www.google.com'},
}

SILKY_AUTHORISATION = True
SILKY_PYTHON_PROFILER = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
KAVEHNEGAR_API = '755A75304B73387A6935775A4633793455754D3847673D3D'

# CELERY STUFF
CELERY_BROKER_URL = 'redis://localhost:{}'.format(REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://localhost:{}'.format(REDIS_PORT)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

ONE_SIGNAL_APP_ID = '2e88f03c-0769-4b2a-b48f-0a1c1b0a9384'

ZOHO_ACCOUNT_ID = '7158925000000008002'
ZOHO_AUTH_TOKEN = '605156151e057de2ac2c19043a23a724'


CONSTANCE_CONFIG = {
    'ANDROID_DIRECT_URL': ('https://canto-app.ir/static/files/android/Canto-v0.9.16-canto.apk', 'Direct Dl link'),
    'ANDROID_DL_COUNT': (0, 'Number of downloads'),
    'ANDROID_MAX': (4, 'Max Version of Android Build Version'),
    'ANDROID_MIN': (1, 'Min Version of Android Build Version'),
    'iOS_MAX': (4, 'Max Version of iOS Build Version'),
    'iOS_MIN': (1, 'Min Version of iOS Build Version'),
    'iOS_SIBAPP_DL': ('https://sibapp.com/applications/canto', 'Sibapp download link'),
    'iOS_NASSAB_DL': ('http://nassaab.com/open/Canto', 'Nassab Download Link'),
    'iOS_UPDATE_LOG': ('', 'new features'),
    'ANDROID_DL': ('', 'Android DownLoad link'),
    'ANDROID_UPDATE_LOG': ('', 'new features'),

    'NASSAB_MAX': (4, 'Max Version of Nassab iOS Build Version'),
    'NASSAB_MIN': (1, 'Min Version of Nassab iOS Build Version'),
    'NASSAB_DL': ('http://nassaab.com/open/Canto', 'Nassab Download Link'),
    'NASSAB_UPDATE_LOG': ('', 'Nassab version new features'),

    'SIBAPP_MAX': (4, 'Max Version of Sibapp iOS Build Version'),
    'SIBAPP_MIN': (1, 'Min Version of Sibapp iOS Build Version'),
    'SIBAPP_DL': ('https://sibapp.com/applications/canto', 'Sibapp download link'),
    'SIBAPP_UPDATE_LOG': ('', 'Sibapp version new features'),

    'CANTO_MAX': (4, 'Max Version of Canto Android Build Version'),
    'CANTO_MIN': (1, 'Min Version of Canto Android Build Version'),
    'CANTO_DL': ('', 'Canto download link'),
    'CANTO_UPDATE_LOG': ('', 'Canto version new features'),

    'GOOGLEPLAY_MAX': (4, 'Max Version of Google Play Android Build Version'),
    'GOOGLEPLAY_MIN': (1, 'Min Version of Google Play Android Build Version'),
    'GOOGLEPLAY_DL': ('', 'Google Play download link'),
    'GOOGLEPLAY_UPDATE_LOG': ('', 'Google Play version new features'),

    'IRANAPPS_MAX': (4, 'Max Version of IRANAPPS Android Build Version'),
    'IRANAPPS_MIN': (1, 'Min Version of IRANAPPS Android Build Version'),
    'IRANAPPS_DL': ('', 'IRANAPPS download link'),
    'IRANAPPS_UPDATE_LOG': ('', 'IRANAPPS version new features'),

    'MYKET_MAX': (4, 'Max Version of MYKET Android Build Version'),
    'MYKET_MIN': (1, 'Min Version of MYKET Android Build Version'),
    'MYKET_DL': ('', 'MYKET download link'),
    'MYKET_UPDATE_LOG': ('', 'MYKET version new features'),

}

CONSTANCE_CONFIG_FIELDSETS = {
    'Direct': ('ANDROID_DIRECT_URL', 'ANDROID_DL_COUNT'),
    'Sibapp': ('SIBAPP_MAX', 'SIBAPP_MIN', 'SIBAPP_DL', 'SIBAPP_UPDATE_LOG'),
    'Nassab': ('NASSAB_MAX', 'NASSAB_MIN', 'NASSAB_DL', 'NASSAB_UPDATE_LOG'),

    'Canto': ('CANTO_MAX', 'CANTO_MIN', 'CANTO_DL', 'CANTO_UPDATE_LOG'),
    'Google-Play': ('GOOGLEPLAY_MAX', 'GOOGLEPLAY_MIN', 'GOOGLEPLAY_DL', 'GOOGLEPLAY_UPDATE_LOG'),
    'IRANAPPS': ('IRANAPPS_MAX', 'IRANAPPS_MIN', 'IRANAPPS_DL', 'IRANAPPS_UPDATE_LOG'),
    'MYKET': ('MYKET_MAX', 'MYKET_MIN', 'MYKET_DL', 'MYKET_UPDATE_LOG'),

    'iOS': ('iOS_MAX', 'iOS_MIN', 'iOS_UPDATE_LOG', 'iOS_SIBAPP_DL', 'iOS_NASSAB_DL'),
    'Android': ('ANDROID_MAX', 'ANDROID_MIN', 'ANDROID_DL', 'ANDROID_UPDATE_LOG')
}


DATADOG_TRACE = {
    'DEFAULT_SERVICE': 'Canto-test',
    'TAGS': {'env': 'test'},
}

VPN_PROXY = {
    "https": 'https://ir434392:797219@us.mybestport.com:443', "http": 'http://ir434392:797219@us.mybestport.com:443'
}


ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}