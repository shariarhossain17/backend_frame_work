"""
Application route definitions
"""
from framework import Application

# Create application instance
app = Application()

@app.route("/home")
def home(request, response):
    """Home route handler"""
    response.text = "Hello from the HOME page"


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

