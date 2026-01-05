from app.app import app

@app.route("/home")
def home(request, response):
    response.text = "Hello from the home Page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from about page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"


@app.route("/sum/{num_1:d}/{num_2:d}")
def sum_numbers(request, response, num_1, num_2):
    total = int(num_1) + int(num_2)
    response.text = f"{num_1} + {num_2} = {total}"

@app.route("/books/{id:d}")
def book_detail(request, response, id):
    response.text = f"Displaying book #{id}"

@app.route("/users/{username:w}/profile")
def user_profile(request, response, username):
    response.text = f"{username}'s profile page"
