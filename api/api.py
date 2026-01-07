from app.app import app

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"

# Class-based handler (new!)
@app.route("/books")
class BooksResource:
    def get(self, req, resp):
        resp.text = "List all books"
    
    def post(self, req, resp):
        resp.text = "Create a new book"

@app.route("/users/{id:d}")
class UserResource:
    def get(self, req, resp, id):
        resp.text = f"Get user {id}"
    
    def put(self, req, resp, id):
        resp.text = f"Update user {id}"
    
    def delete(self, req, resp, id):
        resp.text = f"Delete user {id}"
