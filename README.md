# Code Hacker Framework

A lightweight, modern Python web framework for building fast and flexible web applications and APIs.

## Installation

Install the package using pip:

```bash
pip install code-hacker
```

Or install from source:

```bash
git clone https://github.com/shariarhossain17/backend_frame_work
cd backend_frame_work
pip install -e .
```

## Getting Started After Installation

Once you've installed `code-hacker`, here's how to use it:

```python
from code_hacker import Application as API

# Create your application instance
app = API()

# 1. Function-based route handler
@app.route("/")
def home(request, response):
    response.text = "Hello, World!"

# 2. Route with URL parameters
@app.route("/users/{name}")
def get_user(request, response, name):
    response.json = {"name": name, "message": f"Hello, {name}!"}

# 3. Class-based handler (RESTful style)
@app.route("/books")
class BooksResource:
    def get(self, request, response):
        response.json = {"books": []}

    def post(self, request, response):
        response.json = {"status": "created"}
        response.status_code = 201

# 4. Django-style route registration with method restrictions
def api_handler(request, response):
    response.json = {"data": "API response"}

app.add_route("/api/data", api_handler, allowed_methods=["GET", "POST"])
```

## How to Send Responses

The Code Hacker Framework provides a simple and intuitive response format. **You must follow this format** to send responses correctly.

### Response Format

The `response` object has three main properties for sending different types of responses:

1. **`response.json`** - For JSON responses
2. **`response.html`** - For HTML responses
3. **`response.text`** - For plain text responses

### Priority Order

**Important**: If multiple response properties are set, the priority order is:

1. `response.text` (highest priority)
2. `response.html`
3. `response.json` (lowest priority)

The last property you set will be used for the response.

### JSON Response

Send JSON data using `response.json`. The framework automatically sets the `Content-Type` header to `application/json`.

```python
@app.route("/api/users")
def get_users(request, response):
    response.json = {
        "status": "success",
        "data": {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
    }
```

**Response Format:**

- Content-Type: `application/json`
- Status Code: `200` (default)
- Body: JSON serialized string

### HTML Response

Send HTML content using `response.html`. The framework automatically sets the `Content-Type` header to `text/html`.

```python
@app.route("/")
def index(request, response):
    response.html = "<h1>Welcome to Code Hacker</h1><p>This is an HTML response</p>"
```

**Using Templates:**

```python
@app.route("/home")
def home(request, response):
    response.html = app.template("index.html", context={
        "title": "Home Page",
        "name": "Code Hacker"
    })
```

**Response Format:**

- Content-Type: `text/html`
- Status Code: `200` (default)
- Body: HTML string

### Plain Text Response

Send plain text using `response.text`. The framework automatically sets the `Content-Type` header to `text/plain`.

```python
@app.route("/status")
def status(request, response):
    response.text = "Server is running!"
```

**Response Format:**

- Content-Type: `text/plain`
- Status Code: `200` (default)
- Body: Plain text string

### Custom Status Codes and Headers

You can customize the status code and add custom headers:

```python
@app.route("/created")
def create_resource(request, response):
    response.json = {"message": "Resource created"}
    response.status_code = 201
    response.headers["X-Custom-Header"] = "Custom Value"
```

### Custom Body (Advanced)

For binary data or custom content types:

```python
@app.route("/file")
def download_file(request, response):
    response.body = b"Binary data here"
    response.content_type = "application/octet-stream"
    response.status_code = 200
```

**Response Format Summary:**

| Property        | Content-Type                | Use Case                     |
| --------------- | --------------------------- | ---------------------------- |
| `response.json` | `application/json`          | API responses, data exchange |
| `response.html` | `text/html`                 | Web pages, templates         |
| `response.text` | `text/plain`                | Simple text, status messages |
| `response.body` | Manual (via `content_type`) | Binary data, custom formats  |

## Complete Usage Examples

### Basic Application Setup

```python
from code_hacker import Application as API

app = API()

@app.route("/")
def home(request, response):
    response.text = "Welcome to Code Hacker!"
```

### Routes with Parameters

```python
# String parameter
@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"

# Integer parameter (use :d for digits)
@app.route("/users/{id:d}")
def get_user(request, response, id):
    response.json = {"id": id, "name": f"User {id}"}
```

### Class-Based Handlers (RESTful Style)

```python
@app.route("/books")
class BooksResource:
    def get(self, request, response):
        """Handle GET /books"""
        response.json = {"books": []}

    def post(self, request, response):
        """Handle POST /books"""
        response.json = {"status": "created", "id": 123}
        response.status_code = 201

    def put(self, request, response):
        """Handle PUT /books"""
        response.json = {"status": "updated"}

    def delete(self, request, response):
        """Handle DELETE /books"""
        response.status_code = 204
```

### Django-Style Route Registration

```python
def my_handler(request, response):
    response.text = "Django-style route"

# Register route explicitly
app.add_route("/my-route", my_handler)
```

### HTTP Method Restrictions

```python
# Only allow GET and POST
@app.route("/api/products", allowed_methods=["GET", "POST"])
def products_api(request, response):
    if request.method == "GET":
        response.json = {"products": []}
    elif request.method == "POST":
        response.json = {"status": "created"}
        response.status_code = 201

# Only allow POST
@app.route("/api/submit", allowed_methods=["POST"])
def submit_handler(request, response):
    response.json = {"message": "Submitted successfully"}
```

### Using Templates

**1. Create a template file** (`templates/index.html`):

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>Welcome to {{ name }}</h1>
    <p>{{ description }}</p>
  </body>
</html>
```

**2. Render the template in your route:**

```python
@app.route("/")
def index(request, response):
    response.html = app.template("index.html", context={
        "title": "Home Page",
        "name": "Code Hacker",
        "description": "A modern Python web framework"
    })
```

### Static Files

Static files are automatically served from the `/static` path.

**1. Place files in your static directory:**

```
project/
└── static/
    ├── css/
    │   └── main.css
    └── js/
        └── app.js
```

**2. Reference in templates:**

```html
<link rel="stylesheet" href="/static/css/main.css" />
<script src="/static/js/app.js"></script>
```

### Middleware

Create custom middleware to process requests and responses:

```python
from code_hacker import Application as API, Middleware
import time

app = API()

class TimingMiddleware(Middleware):
    def process_request(self, request):
        # Called before request is handled
        request.start_time = time.time()

    def process_response(self, request, response):
        # Called after request is handled
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response.headers['X-Response-Time'] = f"{duration:.4f}s"

# Register middleware
app.add_middleware(TimingMiddleware)
```

### Exception Handling

Register custom exception handlers:

```python
def custom_exception_handler(request, response, exception):
    response.status_code = 500
    response.json = {
        "error": str(exception),
        "type": type(exception).__name__
    }

app.add_exception_handler(custom_exception_handler)

@app.route("/error")
def error_handler(request, response):
    raise ValueError("Something went wrong!")
```

## Complete Example Application

```python
"""
Complete example application using Code Hacker Framework
"""
from code_hacker import Application as API, Middleware
import time

# Create application
app = API(templates_dir="templates", static_dir="static")

# Custom exception handler
def exception_handler(request, response, exception):
    response.status_code = 500
    response.json = {
        "error": str(exception),
        "type": type(exception).__name__
    }

app.add_exception_handler(exception_handler)

# Timing middleware
class TimingMiddleware(Middleware):
    def process_request(self, req):
        req.start_time = time.time()

    def process_response(self, req, resp):
        if hasattr(req, 'start_time'):
            duration = time.time() - req.start_time
            resp.headers['X-Response-Time'] = f"{duration:.4f}s"

app.add_middleware(TimingMiddleware)

# Routes
@app.route("/")
def home(request, response):
    response.html = app.template("index.html", context={
        "title": "Home",
        "name": "Code Hacker"
    })

@app.route("/api/users")
def get_users(request, response):
    response.json = {
        "status": "success",
        "data": {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
    }

@app.route("/api/users/{id:d}")
class UserResource:
    def get(self, request, response, id):
        response.json = {
            "status": "success",
            "data": {"id": id, "name": f"User {id}"}
        }

    def delete(self, request, response, id):
        response.status_code = 204
        response.text = ""
```

## Using with Production Servers

### Gunicorn

```bash
gunicorn app:app
```

### uWSGI

```bash
uwsgi --http :8000 --wsgi-file app.py
```

### Waitress

```python
from waitress import serve
serve(app, host='0.0.0.0', port=8000)
```

## Testing

Code Hacker includes a built-in test client for easy testing:

```python
import pytest
from code_hacker import Application as API

@pytest.fixture
def api():
    return API()

@pytest.fixture
def client(api):
    return api.test_session()

def test_home_route(api, client):
    @api.route("/")
    def home(request, response):
        response.text = "Hello, World!"

    response = client.get("http://testserver/")
    assert response.text == "Hello, World!"
    assert response.status_code == 200

def test_json_response(api, client):
    @api.route("/api/data")
    def data(request, response):
        response.json = {"key": "value"}

    response = client.get("http://testserver/api/data")
    assert response.json()["key"] == "value"
    assert response.headers["Content-Type"] == "application/json"
```

Run tests:

```bash
pytest test_code_hacker.py
```

## Response Format Reference

### Required Response Format

**You must use one of these properties to send a response:**

```python
# Option 1: JSON Response
response.json = {"key": "value"}
# → Content-Type: application/json

# Option 2: HTML Response
response.html = "<h1>Hello</h1>"
# → Content-Type: text/html

# Option 3: Plain Text Response
response.text = "Hello, World!"
# → Content-Type: text/plain
```

### Response Properties

| Property       | Type      | Description                     | Auto Content-Type           |
| -------------- | --------- | ------------------------------- | --------------------------- |
| `json`         | dict/list | JSON response data              | `application/json`          |
| `html`         | str       | HTML content                    | `text/html`                 |
| `text`         | str       | Plain text content              | `text/plain`                |
| `body`         | bytes     | Raw binary body                 | Manual (set `content_type`) |
| `status_code`  | int       | HTTP status code (default: 200) | -                           |
| `content_type` | str       | Custom content-type header      | -                           |
| `headers`      | dict      | Custom headers dictionary       | -                           |

### Important Notes

1. **Always set exactly one response property** (`json`, `html`, or `text`) for clarity
2. **Status code defaults to 200** if not specified
3. **Content-Type is automatically set** based on the response property used
4. **Priority order**: `text` > `html` > `json` (if multiple are set)
5. **Custom headers** can be added via `response.headers["Header-Name"] = "value"`

## Project Structure

```
project/
├── code_hacker/          # Framework package
│   ├── __init__.py
│   ├── api.py           # Application class
│   ├── middleware.py    # Middleware base class
│   └── response.py      # Response class
├── app.py               # Your application routes
├── conftest.py          # Test fixtures
├── test_code_hacker.py  # Test suite
├── static/              # Static files
│   └── main.css
└── templates/           # Jinja2 templates
    └── index.html
```

## API Reference

### Application Class

#### Constructor

```python
app = API(templates_dir="templates", static_dir="static")
```

- `templates_dir`: Directory containing Jinja2 templates (default: "templates")
- `static_dir`: Directory containing static files (default: "static")

#### Methods

- `route(path, allowed_methods=None)`: Decorator to register a route
- `add_route(path, handler, allowed_methods=None)`: Explicitly register a route
- `add_middleware(middleware_cls)`: Register middleware
- `add_exception_handler(handler)`: Register exception handler
- `template(template_name, context=None)`: Render a Jinja2 template
- `test_session(base_url="http://testserver")`: Create a test client

### Response Object

#### Properties

- `json`: Set JSON response (sets content-type to `application/json`)
- `html`: Set HTML response (sets content-type to `text/html`)
- `text`: Set plain text response (sets content-type to `text/plain`)
- `body`: Set raw body as bytes
- `content_type`: Set content-type header
- `status_code`: Set HTTP status code (default: 200)
- `headers`: Dictionary of custom headers

### Middleware Class

Override these methods in your middleware:

- `process_request(request)`: Called before request handling
- `process_response(request, response)`: Called after request handling

## Requirements

- Python 3.7+
- webob
- jinja2
- whitenoise
- parse
- requests
- wsgiadapter

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.
