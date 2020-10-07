import os

import yaml
import logging
import logging.config
from pythonjsonlogger import jsonlogger

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from dotenv import load_dotenv

def load_envfile(envfile:str="../.env"):
    dotenv_path = os.path.join(os.path.dirname(__file__), envfile)
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        return os.environ
    else:
        raise Exception("Envfile doesn't exist")


load_envfile()



with open('logger_config.yml', 'r') as f:
            config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

logger = logging.getLogger('ui_logger')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY=os.environ.get("SECRET_KEY")

if os.environ.get("ENV_TYPE") != "prod":
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ['31.131.28.206', 'web-api']

DEBUG = os.environ.get("DEBUG")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webui',
]

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'winorbita@gmail.com'
EMAIL_HOST_PASSWORD = '+sh52!fiv'
DEFAULT_MAIL_NAME = "winorbita"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'deploy_static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


env_name = os.getenv('COMPOSE_PROJECT_NAME')

if env_name == 'rel':
    #Sentry-online
    sentry_sdk.init(
        dsn="https://c78be8b64ec64fed8e941e73857c9f45@o430757.ingest.sentry.io/5379863",
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )
else:
    #Sentry-local
    sentry_sdk.init(
        dsn=os.getenv('DSN_SENTRY'),
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
