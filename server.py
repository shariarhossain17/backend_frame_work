from wsgiref.simple_server import make_server

import api.api  # Import routes to register them
from app import app

application =app.middleware

if __name__ =="__main__":
    host="localhost"
    port=8800

    with make_server(host,port,app.middleware) as server:
        print(f"server listening on {host}:{port}")
        server.serve_forever()
