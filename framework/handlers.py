"""
Exception and error handlers
"""
from webob import Request, Response

from .constants import HttpStatus
from .utils import json_response


class CommonHandlers:
    """Common exception handlers for the framework"""
    
    @staticmethod
    def generic_exception_handler(environ, start_response, excp: Exception) -> list[bytes]:
        """
        Generic exception handler for unhandled exceptions
        
        Args:
            environ: WSGI environ dictionary
            start_response: WSGI start_response callable
            excp: The exception that was raised
        
        Returns:
            List of bytes representing the error response
        """
        response = {
            "message": f"Unhandled Exception Occurred: {str(excp)}"
        }

        return json_response(
            response,
            start_response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )

