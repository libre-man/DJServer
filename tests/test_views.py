import pytest
import os
import sys
from .helpers import MockingFunction
from flask import json
from flask.json import JSONDecoder
import datetime

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from server import app as _app
from server import datastore, sessionstore
from server.session import SimpleSession
import server.views as views


@pytest.fixture
def app():
    yield _app.test_client()


def test_index(app):
    page = app.get('/')
    assert page.status_code == 200
    assert views.index() == page.data.decode("utf-8")


@pytest.mark.parametrize("test_data,expected_code", [
    ({'time': 0,
      'data': {'age': 15,
               'gender': 'female'}}, 200),
    ({'time': 100,
      'data': {'age': 15,
               'gender': 'female'}}, 200),
    ({'time': -1,
      'data': {'age': 15,
               'gender': 'female'}}, 200),
    ({'time': 'not_an_int',
      'data': {'age': 15,
               'gender': 'female'}}, 400),
    ({'time': 0,
      'data': {'age': "not an int",
               'gender': 'female'}}, 400),
    ({'time': 0,
      'data': {'age': 5,
               'gender': ['no str']}}, 400),
    ({'time': 0,
      'data': "not a dict"}, 400),
    ({'time': 0,
      'data': ["not a dict"]}, 400),
    ({'time': 0,
      'data': {'age': -5,
               'gender': 'a_str'}}, 400),
])
def test_new_client(app, monkeypatch, test_data, expected_code):
    new_client_mock = MockingFunction(
        func=lambda x: 1 if datastore.validate_new_client(*x) else None,
        pack=True)
    monkeypatch.setattr(datastore, "new_client", new_client_mock)
    page = app.post('/new_client',
                    data=json.dumps(test_data),
                    content_type='application/json')
    assert page.status_code == expected_code
    data = JSONDecoder().decode(page.data.decode('utf-8'))
    assert data['success'] == (expected_code == 200)
    if data['success']:
        input_data = new_client_mock.args[0][0]
        assert input_data[0] == datetime.datetime.fromtimestamp(test_data[
            'time'])
        assert input_data[1] == test_data['data']['age']
        assert input_data[2] == test_data['data']['gender']
        for key, val in input_data[3].items():
            assert test_data['data'][key] == val


@pytest.mark.parametrize("test_data,expected_code", [
    ({'time': 0,
      'data': {'client_id': 1,
               'session_id': 1}}, 200),
    ({'time': -100,
      'data': {'client_id': 1,
               'session_id': 1}}, 200),
    ({'time': "not_an_int",
      'data': {'client_id': 1,
               'session_id': 1}}, 400),
    ({'time': 0,
      'data': {'client_id': "no_int",
               'session_id': 1}}, 400),
    ({'time': 0,
      'data': "not a dict"}, 400),
    ({'time': 0,
      'data': ["not a dict"]}, 400),
    ({'time': 0,
      'data': {'client_id': 1,
               'session_id': "no_an_int"}}, 400),
])
def test_join_session(app, monkeypatch, test_data, expected_code):
    if 'data' in test_data and 'session_id' in test_data['data']:
        sessionstore[test_data['data']['session_id']] = SimpleSession()
    new_client_mock = MockingFunction(lambda: True, simple=True)
    monkeypatch.setattr(datastore, "join_session", new_client_mock)
    page = app.post('/join_session',
                    data=json.dumps(test_data),
                    content_type='application/json')
    print(new_client_mock.args)
    assert page.status_code == expected_code


@pytest.mark.parametrize("test_data,expected_code", [
    ({'time': 0,
      'data': {'client_id': 1,
               'session_id': 1}}, 200),
    ({'time': -100,
      'data': {'client_id': 1,
               'session_id': 1}}, 200),
    ({'time': "not_an_int",
      'data': {'client_id': 1,
               'session_id': 1}}, 400),
    ({'time': 0,
      'data': "not a dict"}, 400),
    ({'time': 0,
      'data': ["not a dict"]}, 400),
])
def test_log_data(app, monkeypatch, test_data, expected_code):
    log_mock = MockingFunction(lambda: True, simple=True)
    monkeypatch.setattr(datastore, 'log', log_mock)
    page = app.post('/log_data',
                    data=json.dumps(test_data),
                    content_type='application/json')
    assert page.status_code == expected_code
    if expected_code == 200:
        assert log_mock.args[0][0][0] == datetime.datetime.fromtimestamp(
            test_data['time'])
        assert log_mock.args[0][0][1] == test_data['data']
