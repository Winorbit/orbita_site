import os
import psycopg2


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'tob9j%nc_2=!*)*h2==&gt7%y%wjvq+h6g%l4@)fp2a@qd_=u*'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','0.0.0.0',"31.131.28.206"]

remoted_db = {'ENGINE': 'django.db.backends.postgresql_psycopg2',
             'NAME': 'orbit_test_db',
             'USER' : 'orbit_test_user',
             'PASSWORD' : 'test_password',
             'HOST' : '31.131.28.206',
             'PORT' : '5432'}

local_db = { 'ENGINE': 'django.db.backends.postgresql_psycopg2',
             'NAME': 'winorbite_alpha',
             'USER' : 'winorbite',
             'PASSWORD' : 'password',
             'HOST' : '127.0.0.1',
             'PORT' : '5432'}


TEST_CONN_PARAMS = {"user": "orbit_test_user", "password": "test_password",  "host": "31.131.28.206" , "port": "5432",  "database": "orbit_test_db"}

def check_remote_conn(db_conn_params):
    conn = psycopg2.connect(**db_conn_params)
    if conn:
        return True
    else:
        return False

def choice_default_db():
    if check_remote_conn(TEST_CONN_PARAMS):
        return remoted_db
    else:
        return local_db
        pass

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'content_app',
    'rest_framework',
    'drf_yasg',
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

ROOT_URLCONF = 'content.urls'

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

WSGI_APPLICATION = 'content.wsgi.application'

DATABASES = {'default': choice_default_db()}

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGE_SIZE': 10
}

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend')
