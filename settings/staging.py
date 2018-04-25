from base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config('CLEARDB_DATABASE_URL')
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv("STRIPE_PUBLISHABLE")
STRIPE_SECRET = os.getenv("STRIPE_SECRET")

SITE_URL = 'https://bibl.herokuapp.com'
ALLOWED_HOSTS.append('bibl.herokuapp.com')

# Log DEBUG information to the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}