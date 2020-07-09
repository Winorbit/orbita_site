from settings.base import *


DEBUG = True

SECRET_KEY = 'tob9j%nc_2=!*)*h2==&gt7%y%wjvq+h6g%l4@)fp2a@qd_=u*'

# SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['31.131.28.206', 'localhost', '127.0.0.1']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'orbit_test_db',
#         'USER' : 'orbit_test_user',
#         'PASSWORD' : 'test_password',
#         'HOST' : '31.131.28.206',
#         'PORT' : '5432'
#     },
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dev_database',
        'USER' : 'dev_user',
        'PASSWORD' : 'qwerty',
        'HOST' : '31.131.28.206',
        'PORT' : '5432'
    },
}