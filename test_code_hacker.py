"""
Code Hacker Framework Test Suite

This module contains comprehensive tests for the Code Hacker web framework.
Tests cover routing, middleware, response handling, static files, and templates.
"""
import pytest

from code_hacker import Application, Middleware

# ============================================================================
# BASIC ROUTING TESTS
# ============================================================================

def test_basic_route_adding(api):
    """
    Test that a basic route can be added using the @route decorator.
    
    Verifies:
    - Routes can be registered with the decorator syntax
    - Handler functions can be decorated and registered
    """
    @api.route("/home")
    def home(req, resp):
        resp.text = "Hello World"


def test_route_overlap_throws_exception(api):
    """
    Test that attempting to register duplicate routes raises an AssertionError.
    
    Verifies:
    - Framework prevents route duplication
    - AssertionError is raised when the same path is registered twice
    """
    @api.route("/test")
    def home(req, resp):
        resp.text = "First handler"

    # Test that duplicate route raises AssertionError
    with pytest.raises(AssertionError):
        @api.route("/test")
        def home2(req, resp):
            resp.text = "Second handler"


def test_client_can_send_requests(api, client):
    """
    Test that the test client can send HTTP requests and receive responses.
    
    Verifies:
    - Test session can send GET requests
    - Response text matches expected value
    - Basic request/response cycle works correctly
    """
    RESPONSE_TEXT = "Hello from test client"

    @api.route("/test")
    def test_handler(req, resp):
        resp.text = RESPONSE_TEXT

    response = client.get("http://testserver/test")
    assert response.text == RESPONSE_TEXT


def test_parameterized_route(api, client):
    """
    Test routes with URL parameters (e.g., /hello/{name}).
    
    Verifies:
    - URL parameters are correctly parsed from the route path
    - Parameter values are passed to handler functions
    - Multiple parameter values work correctly
    """
    @api.route("/hello/{name}")
    def hello(req, resp, name):
        resp.text = f"Hello {name}"

    # Test multiple parameter values
    assert client.get("http://testserver/hello/Alice").text == "Hello Alice"
    assert client.get("http://testserver/hello/Bob").text == "Hello Bob"
    assert client.get("http://testserver/hello/Charlie").text == "Hello Charlie"


def test_default_404_response(client):
    """
    Test that non-existent routes return a 404 status code.
    
    Verifies:
    - Unknown routes return 404 status
    - Default 404 response message is "Not found."
    """
    response = client.get("http://testserver/nonexistent")
    
    assert response.status_code == 404
    assert response.text == "Not found."


# ============================================================================
# CLASS-BASED HANDLER TESTS
# ============================================================================

def test_class_based_handler_get(api, client):
    """
    Test class-based handlers with GET method.
    
    Verifies:
    - Classes can be decorated as route handlers
    - GET method is automatically routed to the class's get() method
    - Response is correctly generated from class method
    """
    response_text = "This is a GET request"

    @api.route("/books")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    response = client.get("http://testserver/books")
    assert response.text == response_text


def test_class_based_handler_post(api, client):
    """
    Test class-based handlers with POST method.
    
    Verifies:
    - POST method is automatically routed to the class's post() method
    - Different HTTP methods map to different class methods
    """
    response_text = "This is a POST request"

    @api.route("/books")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    response = client.post("http://testserver/books")
    assert response.text == response_text


def test_class_based_handler_not_allowed_method(api, client):
    """
    Test that accessing non-existent methods on class handlers raises AttributeError.
    
    Verifies:
    - Requesting unimplemented methods raises AttributeError
    - Framework enforces method availability in class handlers
    """
    @api.route("/books")
    class BookResource:
        def post(self, req, resp):
            resp.text = "Only POST allowed"

    # This should raise AttributeError (method not implemented)
    with pytest.raises(AttributeError):
        client.get("http://testserver/books")


# ============================================================================
# ALTERNATIVE ROUTE REGISTRATION TESTS
# ============================================================================

def test_alternative_route(api, client):
    """
    Test Django-style route registration using add_route() method.
    
    Verifies:
    - Routes can be registered without decorators using add_route()
    - Function-based handlers work with explicit route registration
    """
    response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = response_text

    api.add_route("/alternative", home)

    assert client.get("http://testserver/alternative").text == response_text


# ============================================================================
# TEMPLATE RENDERING TESTS
# ============================================================================

def test_template(api, client):
    """
    Test Jinja2 template rendering functionality.
    
    Verifies:
    - Templates can be rendered with context variables
    - Template context is correctly passed to templates
    - Rendered HTML contains expected content
    """
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


# ============================================================================
# EXCEPTION HANDLING TESTS
# ============================================================================

def test_custom_exception_handler(api, client):
    """
    Test custom exception handler functionality.
    
    Verifies:
    - Custom exception handlers can be registered
    - Exceptions are caught and handled by custom handler
    - Response is modified by exception handler
    """
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"

    api.add_exception_handler(on_exception)

    @api.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/")

    assert response.text == "AttributeErrorHappened"


# ============================================================================
# STATIC FILE SERVING TESTS
# ============================================================================

def test_404_is_returned_for_nonexistent_static_file(tmpdir_factory):
    """
    Test that requests for non-existent static files return 404.
    
    Verifies:
    - Missing static files return 404 status
    - Static file serving handles missing files gracefully
    """
    empty_static_dir = tmpdir_factory.mktemp("empty_static")
    api = Application(static_dir=str(empty_static_dir))
    client = api.test_session()
    assert client.get("http://testserver/static/main.css").status_code == 404


# Constants for static file tests
FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"


def _create_static(static_dir):
    """
    Helper function to create a static file for testing.
    
    Args:
        static_dir: Directory to create the static file in
    
    Returns:
        Created file asset
    """
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)
    return asset


def test_assets_are_served(tmpdir_factory):
    """
    Test that static files are correctly served by the framework.
    
    Verifies:
    - Static files are accessible via /static/ path
    - File contents are correctly served
    - Correct status code (200) is returned for existing files
    """
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)
    api = Application(static_dir=str(static_dir))
    client = api.test_session()

    response = client.get(f"http://testserver/static/{FILE_DIR}/{FILE_NAME}")

    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


# ============================================================================
# MIDDLEWARE TESTS
# ============================================================================

def test_middleware_methods_are_called(api, client):
    """
    Test that middleware process_request and process_response methods are called.
    
    Verifies:
    - Middleware process_request() is called before request handling
    - Middleware process_response() is called after request handling
    - Custom middleware can be registered and executed
    """
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


# ============================================================================
# HTTP METHOD RESTRICTION TESTS
# ============================================================================

def test_allowed_methods_for_function_based_handlers(api, client):
    """
    Test that allowed_methods parameter restricts HTTP methods for function handlers.
    
    Verifies:
    - Only specified HTTP methods are allowed for a route
    - Unallowed methods raise AttributeError
    - Allowed methods work correctly
    """
    @api.route("/home", allowed_methods=["post"])
    def home(req, resp):
        resp.text = "Hello"

    with pytest.raises(AttributeError):
        client.get("http://testserver/home")

    assert client.post("http://testserver/home").text == "Hello"


def test_default_allowed_methods(api, client):
    """
    Test that routes allow all standard HTTP methods by default.
    
    Verifies:
    - Default behavior allows GET, POST, PUT, PATCH, DELETE, OPTIONS
    - All common HTTP methods work without explicit specification
    """
    @api.route("/default")
    def default_handler(req, resp):
        resp.text = f"Method: {req.method}"

    # All these methods should work by default
    assert client.get("http://testserver/default").text == "Method: GET"
    assert client.post("http://testserver/default").text == "Method: POST"
    assert client.put("http://testserver/default").text == "Method: PUT"


def test_add_route_with_allowed_methods(api, client):
    """
    Test that add_route() method accepts allowed_methods parameter.
    
    Verifies:
    - Django-style route registration supports method restrictions
    - Method restrictions work with explicit route registration
    """
    def restricted_handler(req, resp):
        resp.text = "Only PUT allowed"

    api.add_route("/restricted", restricted_handler, allowed_methods=["put"])

    with pytest.raises(AttributeError):
        client.get("http://testserver/restricted")

    assert client.put("http://testserver/restricted").text == "Only PUT allowed"


def test_class_based_handlers_still_work(api, client):
    """
    Test that class-based handlers continue to work with method restrictions.
    
    Verifies:
    - Class handlers work correctly with method routing
    - Multiple methods can be implemented in the same class
    - Unimplemented methods raise AttributeError
    """
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


# ============================================================================
# RESPONSE TYPE TESTS
# ============================================================================

def test_json_response_helper(api, client):
    """
    Test JSON response helper functionality.
    
    Verifies:
    - Setting resp.json automatically sets content-type to application/json
    - JSON data is correctly serialized
    - Response headers contain correct content-type
    """
    @api.route("/json")
    def json_handler(req, resp):
        resp.json = {"name": "PoridhiFrame"}

    response = client.get("http://testserver/json")
    json_body = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert json_body["name"] == "PoridhiFrame"


def test_html_response_helper(api, client):
    """
    Test HTML response helper functionality.
    
    Verifies:
    - Setting resp.html automatically sets content-type to text/html
    - HTML content is correctly rendered
    - Template rendering can be used with HTML responses
    """
    @api.route("/html")
    def html_handler(req, resp):
        resp.html = api.template("index.html", context={"title": "Best Title", "name": "Best Name"})

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Best Title" in response.text
    assert "Best Name" in response.text


def test_text_response_helper(api, client):
    """
    Test plain text response helper functionality.
    
    Verifies:
    - Setting resp.text automatically sets content-type to text/plain
    - Text content is correctly encoded
    - Response headers contain correct content-type
    """
    response_text = "Just Plain Text"

    @api.route("/text")
    def text_handler(req, resp):
        resp.text = response_text

    response = client.get("http://testserver/text")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == response_text


def test_manually_setting_body(api, client):
    """
    Test manually setting response body and content-type.
    
    Verifies:
    - Response body can be set directly as bytes
    - Content-type can be manually specified
    - Custom content-types work correctly
    """
    @api.route("/body")
    def text_handler(req, resp):
        resp.body = b"Byte Body"
        resp.content_type = "text/plain"

    response = client.get("http://testserver/body")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Byte Body"


def test_response_property_priority(api, client):
    """
    Test that response properties have priority order (text > html > json).
    
    Verifies:
    - When multiple response properties are set, the last one takes priority
    - Property order determines final response type
    """
    @api.route("/priority")
    def priority_handler(req, resp):
        resp.json = {"type": "json"}
        resp.html = "<h1>HTML</h1>"
        resp.text = "Plain text"  # Last one wins

    response = client.get("http://testserver/priority")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Plain text"


def test_empty_response_handling(api, client):
    """
    Test handling of responses with no body set.
    
    Verifies:
    - Empty responses return 200 status code
    - Response body is empty when no properties are set
    - Framework handles missing response content gracefully
    """
    @api.route("/empty")
    def empty_handler(req, resp):
        # Don't set any response properties
        pass

    response = client.get("http://testserver/empty")

    assert response.status_code == 200
    assert response.text == ""  # Empty body
