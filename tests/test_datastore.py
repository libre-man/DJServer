import pytest
import sys
import os
from .helpers import MockingFunction
from datetime import datetime

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from server.datastore import SimpleDatastore


@pytest.fixture
def simple_datastore():
    yield SimpleDatastore()


def test_simpledatastore(simple_datastore):
    assert isinstance(simple_datastore, SimpleDatastore)


@pytest.fixture(params=[1, True, None, '5', {}, []])
def client_id(request):
    yield request.param


@pytest.fixture(params=[1, True, False, None, '5', {}, []])
def session_id(request):
    yield request.param


@pytest.mark.parametrize("data,expected", [
    ([datetime.now(), 10, "female", None], True),
    ([datetime.now(), 1000, "female", None], True),
    ([datetime.now(), 1000, "female", {0: 1,
                                       2: 3}], True),
    ([datetime.now(), 1000, -1, None], False),
    (["No datetime", 10, "female", None], False),
    ([datetime.now(), -1, "female", None], False),
    ([datetime.now(), "no int", "female", None], False),
    (["no datetime", "no int", -1, None], False),
])
def test_validate_new_client(simple_datastore, data, expected):
    assert simple_datastore.validate_new_client(*data) == expected


@pytest.mark.parametrize("data,return_val,expected", [(
    [1, 2, 3, 4], True, 1), ([1, 2, 3], True, 1), ([1, 2, 3, 4], False, None)])
def test_simple_new_client(simple_datastore, monkeypatch, data, return_val,
                           expected):
    mock_validate_new_client = MockingFunction(lambda: return_val, simple=True)
    monkeypatch.setattr(simple_datastore, "validate_new_client",
                        mock_validate_new_client)
    assert simple_datastore.new_client(*data) == expected
    if return_val:
        if len(data) == 3:
            data.append(None)
        assert mock_validate_new_client.args[0][0][0] == expected


def test_simple_client_exisits(simple_datastore, client_id):
    assert simple_datastore.client_exists(client_id)


def test_simple_join_session(simple_datastore, client_id, session_id):
    assert simple_datastore.join_session(client_id, session_id)


def test_simple_log(simple_datastore):
    assert simple_datastore.log(None, None)
