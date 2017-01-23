from .base import *

DEBUG = True

ALLOWED_HOSTS = ['sdaas.yovo.nl', 'www.sdaas.yovo.nl', 'sdaas.nl', '10.1.10.181',
                 'www.sdaas.nl', 'testserver', '127.0.0.1', 'localhost', '0.0.0.0', '10.200.10.1', '145.109.62.56']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
