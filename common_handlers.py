
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
    @staticmethod
    def request_handler(routes,request):

        response =Response()
        route_found = False
        for path,handler in routes.items():
            if path==request.path:
                handler(request,response)
                route_found = True
                break
            
        if not route_found:
            response.status = HttpStatus.NOT_FOUND
            response.text = "Route not found"
      
        return response    