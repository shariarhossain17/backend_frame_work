"""
Application route definitions
"""
from framework import Application,Middleware

# Create application instance
app = Application(templates_dir="templates")


def custom_exception_handler(request, response, exception_cls):
    response.text = f"Error occurred: {str(exception_cls)}"

app.add_exception_handler(custom_exception_handler)

@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")



@app.route("/home")
def home(request, response):
    """Home route handler"""
    response.text = "Hello from the HOME page"



@app.route("/template")
def page_handler(req, resp):
    resp.body = app.template("index.html", context={
        "name": "beckend frame work", 
        "title": "Best Framework"
    }).encode()


#django style route

def sample_handler(req,res):
    res.text="Django style route reigistration"

app.add_route("/sample",sample_handler)


@app.route("/hello/{name}")
def greeting(request, response, name):
    """Greeting route handler with parameter"""
    response.text = f"Hello, {name}!"

# Class-based handler
@app.route("/books")
class BooksResource:
    """Books resource with multiple HTTP methods"""
    
    def get(self, req, resp):
        """GET /books - List all books"""
        resp.text = "List all books"
    
    def post(self, req, resp):
        """POST /books - Create a new book"""
        resp.text = "Create a new book"

@app.route("/users/{id:d}")
class UserResource:
    """User resource with integer ID parameter"""
    
    def get(self, req, resp, id):
        """GET /users/{id} - Get user by ID"""
        resp.text = f"Get user {id}"
    
    def put(self, req, resp, id):
        """PUT /users/{id} - Update user by ID"""
        resp.text = f"Update user {id}"
    
    def delete(self, req, resp, id):
        """DELETE /users/{id} - Delete user by ID"""
        resp.text = f"Delete user {id}"


# add middleware

class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, resp):
        print("Processing response", req.url)

app.add_middleware(SimpleCustomMiddleware)

app.ad

