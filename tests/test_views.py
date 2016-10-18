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
    page = app.get('/')
    assert page.status_code == 200
    assert views.index() == page.data.decode("utf-8")


def test_new_client(app):
    page = app.get('/new_client')
    assert page.status_code == 200
    assert views.new_client() == page.data.decode('utf-8')


def test_join_session(app):
    page = app.get('/join_session')
    assert page.status_code == 200
    assert views.join_session() == page.data.decode('utf-8')


def test_log_data(app):
    page = app.get('/log_data')
    assert page.status_code == 200
    assert views.log_data() == page.data.decode('utf-8')
