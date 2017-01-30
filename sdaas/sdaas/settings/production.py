from .base import *

from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


ALLOWED_HOSTS = ['sdaas.yovo.nl', 'www.sdaas.yovo.nl', 'sdaas.nl',
                 'www.sdaas.nl', '127.0.0.1', 'localhost']

#STATIC_ROOT = get_env_setting('STATIC_ROOT')
STATIC_ROOT = "/home/yourivoet/public/sdaas.nl/sdaas/static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            # get_env_setting('DATABASE_CNF')
            'read_default_file': "/home/yourivoet/public/sdaas.nl/db.cnf",
        },
    }
}

CONTROLLER_URL = 'http://sdaas.nl'
OUTPUT_DIR = '/home/yourivoet/public/controller.sdaas.nl/public/'
