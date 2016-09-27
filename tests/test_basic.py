import nose.tools
import os
import sys

sys.path.insert(0, os.path.abspath('..'))


def setup():
    print("SETUP!")


def teardown():
    print("TEAR DOWN!")


def test_basic():
    print("I RAN!")
