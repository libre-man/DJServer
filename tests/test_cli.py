import pytest
import os
import sys
from .helpers import MockingFunction

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

from server import app
import server.cli as cli


@pytest.mark.parametrize("debug", [True, False])
def test_main(capsys, debug, monkeypatch):
    mock_run = MockingFunction()
    monkeypatch.setattr(app, "run", mock_run)
    cli.main(debug=debug)
    assert mock_run.called
    assert mock_run.args[0][1]['debug'] == debug
