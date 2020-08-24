import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


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

#Sentry-online
sentry_sdk.init(
    dsn="https://c78be8b64ec64fed8e941e73857c9f45@o430757.ingest.sentry.io/5379863",
    integrations=[DjangoIntegration()],
    send_default_pii=True
)