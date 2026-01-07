"""
Core Application class for the framework
"""
from webob import Request, Response
from parse import parse
import inspect
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from .constants import HttpStatus


class Application:
    """
    Main WSGI application class
    
    Handles routing, request processing, and response generation.
    """
    
    def __init__(self):
        """Initialize the application with an empty route dictionary"""
        self.routes = {}

    """ add test client session"""

    def test_session(self,base_url="http://testserver"):
        session=RequestsSession()
        session.mount(prefix=base_url,adapter=RequestsWSGIAdapter(self))
        return session

    def __call__(self, environ, start_response):
        """
        WSGI application interface
        
        Args:
            environ: WSGI environ dictionary
            start_response: WSGI start_response callable
        
        Returns:
            Response from handle_request
        """
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def route(self, path):
        """
        Decorator for registering routes
        
        Args:
            path: URL path pattern (supports parse-style patterns)
        
        Returns:
            Decorator function that registers the handler
        
        Example:
            @app.route("/home")
            def home(request, response):
                response.text = "Hello"
        """
        assert path not in self.routes, "Such route already exists."
        
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper
    
    def default_response(self, response):
        """
        Set default 404 response
        
        Args:
            response: Response object to modify
        """
        response.status_code = HttpStatus.NOT_FOUND
        response.text = "Route Not found."
    
    def find_handler(self, request_path):
        """
        Find a handler for the given request path
        
        Args:
            request_path: The path from the request
        
        Returns:
            Tuple of (handler, kwargs_dict) or (None, None) if not found
        """
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None
  
    def handle_request(self, request):
        """
        Process a request and generate a response
        
        Args:
            request: WebOb Request object
        
        Returns:
            WebOb Response object
        """
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        
        if handler is not None:
            if inspect.isclass(handler):
                # Class-based handler - get method based on HTTP verb
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)
            
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
            
        return response

