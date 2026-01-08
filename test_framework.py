"""
Framework tests
"""
import pytest

from framework import Application,Middleware


def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "Hello World"

def test_route_overlap_throws_exception(api):
    @api.route("/test")
    def home(req, resp):
        resp.text = "First handler"

    # Test that duplicate route raises AssertionError
    with pytest.raises(AssertionError):
        @api.route("/test")
        def home2(req, resp):
            resp.text = "Second handler"

def test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "Hello from test client"

    @api.route("/test")
    def test_handler(req, resp):
        resp.text = RESPONSE_TEXT

    response = client.get("http://testserver/test")
    assert response.text == RESPONSE_TEXT

def test_parameterized_route(api, client):
    @api.route("/hello/{name}")
    def hello(req, resp, name):
        resp.text = f"Hello {name}"

    # Test multiple parameter values
    assert client.get("http://testserver/hello/Alice").text == "Hello Alice"
    assert client.get("http://testserver/hello/Bob").text == "Hello Bob"
    assert client.get("http://testserver/hello/Charlie").text == "Hello Charlie"

def test_default_404_response(client):
    response = client.get("http://testserver/nonexistent")
    
    assert response.status_code == 404
    assert response.text == "Not found."

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

def test_custom_exception_handler(api, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"

    api.add_exception_handler(on_exception)

    @api.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/")

    assert response.text == "AttributeErrorHappened"

def test_404_is_returned_for_nonexistent_static_file(tmpdir_factory):
    empty_static_dir = tmpdir_factory.mktemp("empty_static")
    api = Application(static_dir=str(empty_static_dir))
    client = api.test_session()
    assert client.get("http://testserver/static/main.css").status_code == 404

FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"

def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)
    return asset

def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)
    api = Application(static_dir=str(static_dir))
    client = api.test_session()

    response = client.get(f"http://testserver/static/{FILE_DIR}/{FILE_NAME}")

    assert response.status_code == 200
    assert response.text == FILE_CONTENTS



def test_middleware_methods_are_called(api, client):
    process_request_called = False
    process_response_called = False

    class CallMiddlewareMethods(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, resp):
            nonlocal process_response_called
            process_response_called = True

    api.add_middleware(CallMiddlewareMethods)

    @api.route('/')
    def index(req, resp):
        resp.text = "YOLO"

    client.get('http://testserver/')

    assert process_request_called is True
    assert process_response_called is True



def test_allowed_methods_for_function_based_handlers(api, client):
    @api.route("/home", allowed_methods=["post"])
    def home(req, resp):
        resp.text = "Hello"

    with pytest.raises(AttributeError):
        client.get("http://testserver/home")

    assert client.post("http://testserver/home").text == "Hello"





def test_default_allowed_methods(api, client):
    @api.route("/default")
    def default_handler(req, resp):
        resp.text = f"Method: {req.method}"

    # All these methods should work by default
    assert client.get("http://testserver/default").text == "Method: GET"
    assert client.post("http://testserver/default").text == "Method: POST"
    assert client.put("http://testserver/default").text == "Method: PUT"

def test_add_route_with_allowed_methods(api, client):
    def restricted_handler(req, resp):
        resp.text = "Only PUT allowed"

    api.add_route("/restricted", restricted_handler, allowed_methods=["put"])

    with pytest.raises(AttributeError):
        client.get("http://testserver/restricted")

    assert client.put("http://testserver/restricted").text == "Only PUT allowed"

def test_class_based_handlers_still_work(api, client):
    @api.route("/resource")
    class TestResource:
        def get(self, req, resp):
            resp.text = "GET method"
        
        def post(self, req, resp):
            resp.text = "POST method"

    assert client.get("http://testserver/resource").text == "GET method"
    assert client.post("http://testserver/resource").text == "POST method"
    
    # PUT not implemented - should raise AttributeError
    with pytest.raises(AttributeError):
        client.put("http://testserver/resource")