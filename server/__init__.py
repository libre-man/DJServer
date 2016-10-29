from flask import Flask
from .datastore import SimpleDatastore
from .session import SimpleSessionstore

app = Flask(__name__)
datastore = SimpleDatastore()
sessionstore = SimpleSessionstore()

import server.views
