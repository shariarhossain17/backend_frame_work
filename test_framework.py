import pytest
from app import middleware


@pytest.fixture
def api():
    return middleware

def test_basic_route_adding(api):
    @api.route("/home")
    def home(req,res):
        res.text="Hello world"