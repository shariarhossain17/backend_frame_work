from wsgiref.simple_server import make_server

from app import app

if __name__ =="__main__":
    host="localhost"
    port=8800

    with make_server(host,port,app.app) as server:
        print(f"server listening on {host}:{port}")
        server.serve_forever()
