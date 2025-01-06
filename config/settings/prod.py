from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ""
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME' : os.getenv('DB_SCHEMA'),
        'USER' : os.getenv('DB_USERNAME'),
        'PASSWORD' : os.getenv('DB_PASSWORD'),
        'HOST' : os.getenv('DB_HOST'),
        'PORT' : '5432',
    }
}