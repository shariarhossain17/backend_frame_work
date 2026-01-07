"""
Application entry point
"""
from wsgiref.simple_server import make_server
from api import middleware


app=middleware


if __name__ == "__main__":
    host = "localhost"
    port = 8000

    with make_server(host, port, middleware) as server:
        print(f"Server listening on {host}:{port}")
        server.serve_forever()

