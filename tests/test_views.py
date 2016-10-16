import pytest
import os
import sys
from .helpers import MockingFunction

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from server import app as _app
import server.views as views

@pytest.fixture
def app():
    yield _app.test_client()

def test_index(app):
    index = app.get('/')
    assert index.status_code == 200
    assert views.index() == index.data.decode("utf-8")
