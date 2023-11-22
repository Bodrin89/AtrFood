import logging
import os
from pathlib import Path
from datetime import timedelta

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# from django.conf.locale import LANG_INFO

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS'), '*']

DJANGO_APPS = [
    'dal',
    'dal_select2',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'drf_yasg',
]

LOCAL_APPS = [
    'apps.user',
    'apps.individual_user',
    'apps.company_user',
    'apps.product',
    'apps.review',
    'apps.cart',
    'apps.promotion',
    'apps.order',
    'apps.clients',
    'apps.library',
    'apps.blog',
    'apps.document',
    'apps.notes',
    'apps.tg_bot',
    'apps.administrative_staff',
    'apps.payment',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)


CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': 5432,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

LANGUAGE_CODE = 'ru'

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
# MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'en'

# LANG_INFO = {
#     'kz': {
#         'bidi': False,
#         'code': 'kz',
#         'name': 'Kazakh',
#         'name_local': 'Қазақ',
#     },
#     'ru': {
#         'bidi': False,
#         'code': 'ru',
#         'name': 'Russian',
#         'name_local': 'Русский',
#     },
# }

LANGUAGES = [
    ('ru', _('Russian')),
    ('kk', _('Kazakh')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'apps/locale'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.BaseUserModel'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_format': {
            'format': '{asctime} - {levelname} - {module} - {filename} - {lineno} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_format',
            'level': 'WARNING'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'main_format',
            'filename': 'log.log',
            'maxBytes': 1000 * 1024 * 10,
            'backupCount': 5
        }
    },
    'loggers': {
        'main': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

LOGGER = logging.getLogger('main')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('SMTP_HOST')
EMAIL_PORT = int(os.getenv('SMTP_PORT'))
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_HOST_USER = os.getenv('SMTP_USER')
EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASSWORD')

CELERY_BROKER_URL = os.getenv('REDIS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

BOT_TOKEN = os.getenv('BOT_TOKEN')

TIME_CACHE_TG_BOT_MESSAGE = 60 * 60  # Время хранения кэша сообщений телеграм бота

DEFAULT_MASSAGE_BOT = {
    'introductory_message': 'добро пожаловать в магазин ArtFood',
    'message_after_hours': 'Магазин закрыт, обратитесь в рабочее время',
    'message_order_not_site': 'для того чтобы воспользоваться доставкой вам требуется приобрести товар на нашем сайте',
    'introductory_message_anonymous': 'Добро пожаловать в магазин ArtFood Если вы не зарегистрированы, пройдите '
                                      'регистрацию на сайте Если вы зарегистрированы, введите ваш email Для отмены '
                                      'нажмите "cancel"',
}

if DEBUG:
    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=4000),
    }