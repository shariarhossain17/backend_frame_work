"""
API routes package
"""
from .routes import app
from framework import ErrorHandlerMiddleWare, CommonHandlers

# Create middleware-wrapped application
middleware = ErrorHandlerMiddleWare(
    app=app,
    exception_handler=CommonHandlers.generic_exception_handler
)

__all__ = ['app', 'middleware']

