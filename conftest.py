import pytest

from code_hacker import Application



@pytest.fixture
def api():
    """Fixture that provides the middleware-wrapped application"""
    return Application()


@pytest.fixture
def client(api):
    return api.test_session()