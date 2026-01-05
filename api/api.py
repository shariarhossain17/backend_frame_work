from app.app import app

@app.route("/home")
def home(request, response):
    response.text = "Hello from the home Page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from about page"
