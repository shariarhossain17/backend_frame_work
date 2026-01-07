import pytest

from framework import Application



@pytest.fixture
def api():
    """Fixture that provides the middleware-wrapped application"""
    return Application()
