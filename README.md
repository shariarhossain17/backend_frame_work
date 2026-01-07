# Backend Framework

A lightweight WSGI web framework built with Python.

## Project Structure

```
backend_frame_work/
├── framework/              # Core framework code
│   ├── __init__.py        # Framework exports
│   ├── app.py             # Application class (routing, request handling)
│   ├── middleware.py      # Middleware classes
│   ├── handlers.py        # Exception handlers
│   ├── utils.py           # Utility functions
│   └── constants.py       # HTTP status constants
├── api/                   # Application routes
│   ├── __init__.py        # API exports (app, middleware)
│   └── routes.py          # Route definitions
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_framework.py  # Framework tests
└── run.py                 # Application entry point
```

## Usage

### Running the Server

```bash
python run.py
```

The server will start on `localhost:8000`.

### Defining Routes

Routes are defined in `api/routes.py`:

```python
from framework import Application

app = Application()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/users/{id:d}")
class UserResource:
    def get(self, req, resp, id):
        resp.text = f"Get user {id}"
```

### Running Tests

```bash
pytest tests/
```

## Framework Components

- **Application**: Core WSGI application with routing support
- **ErrorHandlerMiddleWare**: Middleware for exception handling
- **CommonHandlers**: Exception handler utilities
- **Utils**: Helper functions for JSON responses
- **Constants**: HTTP status code constants
