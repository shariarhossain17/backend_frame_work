class Application:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        response_body = 'hello from server'
        status = '200 OK'
        headers = [
            ('Content-Type', 'text/plain; charset=utf-8')
        ]

        start_response(status, headers)
        return [response_body.encode('utf-8')]


app = Application()
