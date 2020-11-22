"""Tests random functions.

pytest will fail in case there aren't any tests in the code.
"""


def foo():
    """Fetch some data to test."""
    return True


def test_foo():
    """Tests the function."""
    assert foo()
