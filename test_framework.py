"""
Framework tests
"""
import pytest



def test_class_based_handler_get(api, client):
    response_text = "This is a GET request"

    @api.route("/books")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    response = client.get("http://testserver/books")
    assert response.text == response_text

def test_class_based_handler_post(api, client):
    response_text = "This is a POST request"

    @api.route("/books")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    response = client.post("http://testserver/books")
    assert response.text == response_text

def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/books")
    class BookResource:
        def post(self, req, resp):
            resp.text = "Only POST allowed"

    # This should raise AttributeError (method not implemented)
    with pytest.raises(AttributeError):
        client.get("http://testserver/books")

def test_alternative_route(api, client):
    response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = response_text

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text


def test_template(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.body = api.template("index.html", context={
            "title": "Some Title", 
            "name": "Some Name"
        }).encode()

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Some Title" in response.text
    assert "Some Name" in response.text
