try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A server that is an end point for the magenta clients',
    'author': 'Thomas Schaper',
    'url': 'https://gitlab.com/SilentDiscoAsAService/Server',
    'download_url': 'https://gitlab.com/SilentDiscoAsAService/Server',
    'author_email': 'thomas@libremail.nl',
    'version': '0.0',
    'install_requires': ['nose'],
    'packages': ['server'],
    'scripts': [],
    'name': 'server'
}

setup(**config)