from wsgiref.simple_server import make_server


class Reverseware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        result = self.app(environ, start_response)
        reversed_result = [chunk[::-1] for chunk in result]
        if hasattr(result, 'close'):
            reversed_result.close = result.close
        return reversed_result


def application(environ, start_response):
    response_body = [
        f'{key} : {value}' for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain; charset=utf-8')
    ]
    start_response(status, headers)

    return [response_body.encode('utf-8')]


server = make_server('localhost', 8000, Reverseware(application))
print("Server running on http://localhost:8000")
server.serve_forever()
