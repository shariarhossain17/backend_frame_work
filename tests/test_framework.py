"""
Framework tests
"""
import pytest
from framework import Application



@pytest.fixture
def api():
    """Fixture that provides the middleware-wrapped application"""
    return Application()


def test_basic_route_adding(api):
    """Test that routes can be added to the application"""
    @api.route("/home")
    def home(req, res):
        res.text = "Hello world"

