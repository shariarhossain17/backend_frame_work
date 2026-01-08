"""
Middleware classes for the framework
"""
class ErrorHandlerMiddleWare:
    """
    Middleware for handling exceptions in WSGI applications
    
    Wraps an application and catches any exceptions, passing them
    to a configured exception handler.
    """
    
    def __init__(self, app, exception_handler: callable):
        """
        Initialize the error handler middleware
        
        Args:
            app: The WSGI application to wrap
            exception_handler: Callable that handles exceptions
        """
        self.wrapped_app = app
        self.exception_handler = exception_handler

    def __call__(self, environ, start_response):
        """
        WSGI application interface
        
        Args:
            environ: WSGI environ dictionary
            start_response: WSGI start_response callable
        
        Returns:
            Response from wrapped app or exception handler
        """
        try:
            return self.wrapped_app(environ, start_response)
        except Exception as e:
            return self.exception_handler(environ, start_response, e)
    
    def __getattr__(self, name):
        """
        Delegate attribute access to the wrapped app
        
        This allows the middleware to be used as a transparent proxy,
        so methods like route() can be called directly on the middleware.
        """
        return getattr(self.wrapped_app, name)

