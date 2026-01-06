"""
Framework tests
"""
import pytest
from api import middleware


@pytest.fixture
def api():
    """Fixture that provides the middleware-wrapped application"""
    return middleware


def test_basic_route_adding(api):
    """Test that routes can be added to the application"""
    @api.route("/home")
    def home(req, res):
        res.text = "Hello world"

