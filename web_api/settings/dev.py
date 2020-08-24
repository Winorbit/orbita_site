import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = True

SECRET_KEY = 'tob9j%nc_2=!*)*h2==&gt7%y%wjvq+h6g%l4@)fp2a@qd_=u*'

# SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['31.131.28.206', 'web-api', '127.0.0.1', '0.0.0.0']

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

#Sentry-local
sentry_sdk.init(
    dsn=os.getenv('DSN_SENTRY'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)