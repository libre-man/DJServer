from .base import *

DEBUG = True

ALLOWED_HOSTS = ['sdaas.yovo.nl', 'www.sdaas.yovo.nl', 'sdaas.nl',
                 'www.sdaas.nl', 'testserver', '127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
