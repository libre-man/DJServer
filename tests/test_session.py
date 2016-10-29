import pytest
import sys
import os

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from server.session import SimpleSession, SimpleSessionstore


@pytest.fixture
def simple_sessionstore():
    yield SimpleSessionstore()


@pytest.fixture(params=['Test12', None])
def simple_session(request):
    if request.param is not None:
        yield SimpleSession(name=request.param)
    else:
        yield SimpleSession()


def test_dimple_session_store(simple_sessionstore, simple_session):
    assert isinstance(simple_sessionstore, SimpleSessionstore)
    assert isinstance(simple_sessionstore, dict)
    assert 0 in simple_sessionstore
    assert isinstance(simple_sessionstore[0], SimpleSession)
    simple_sessionstore[1] = simple_session
    assert simple_sessionstore[1] == simple_session
