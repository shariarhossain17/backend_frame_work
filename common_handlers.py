
from constant import HttpStatus
from helper import json_response
from webob import Response,Request


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
    @staticmethod
    def request_handler(routes,request):

        response =Response()
        for path,handler in routes.items():
            if path==request.path:
                handler(request,response)
            
      
        return response    