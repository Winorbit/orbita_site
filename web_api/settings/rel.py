from settings.base import *


DEBUG = False

SECRET_KEY = 'tob9j%nc_2=!*)*h2==&gt7%y%wjvq+h6g%l4@)fp2a@qd_=u*'

# SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['31.131.28.206', 'web-api', '127.0.0.1', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'release_database',
        'USER' : 'release_user',
        'PASSWORD' : 'releaseqwerty',
        'HOST' : '31.131.28.206',
        'PORT' : '5432'
    },
}