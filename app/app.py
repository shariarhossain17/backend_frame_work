from common_handlers import CommonHandlers
from helper import json_response
from middlewares import ErrorHandlerMiddleWare
from webob import Request, Response
from helper import json_response

class Application:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = CommonHandlers.request_handler(self.routes, request)
        return json_response(response,start_response)
    

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
    
  

app = Application()
middleware = ErrorHandlerMiddleWare(
    app=app,
    exception_handler=CommonHandlers.generic_exception_handler
)
