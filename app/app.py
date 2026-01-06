from common_handlers import CommonHandlers
from helper import json_response
from middlewares import ErrorHandlerMiddleWare
from webob import Request, Response
from constant import HttpStatus
from parse import parse

class Application:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response) 
    

    def route(self, path):
        assert path not in self.routes, "Such route already exists."
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper
    
    def default_response(self, response):
        response.status_code = HttpStatus.NOT_FOUND
        response.text = "Route Not found."
    
    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None
  
    def handle_request(self, request):
        response = Response()
        
        handler, kwargs = self.find_handler(request_path=request.path)
        
        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
            
        return response
    

    
  

app = Application()
middleware = ErrorHandlerMiddleWare(
    app=app,
    exception_handler=CommonHandlers.generic_exception_handler
)
