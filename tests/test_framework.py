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

def test_route_overlap_throws_exception(api):
    @api.route("/test")
    def home(req,res):
        res.text="first handler"
    
    with pytest.raises(AssertionError):
        @api.route("/test")
        def home2(req,res):
            res.text="second handler"

