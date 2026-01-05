
from webob import Request, Response

from constant import HttpStatus
from helper import json_response


class CommonHandlers:
    @staticmethod
    def generic_exception_handler(environ,start_response,excp:Exception)->list[bytes]:
        response={
            "message": f"Unhanded Exception Occurred :{str(excp)}"
        }

        return json_response(
            response,
            start_response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )
