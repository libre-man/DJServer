import os
import pytest

class MockingFunction():
    def __init__(self, func=None):
        self.called = False
        self.args = list()
        self.func = func

    def __call__(self, *args, **kwargs):
        self.called = True
        self.args.append((args, kwargs))
        if self.func is not None:
            return self.func(*args, **kwargs)