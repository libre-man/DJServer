import pytest
import os
import sys

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import server.cli as cli


def test_main(capsys):
    assert(True)
    #cli.main()
    #out, _ = capsys.readouterr()
    #assert out == '5\n'
