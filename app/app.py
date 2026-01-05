from common_handlers import CommonHandlers
from helper import json_response
from middlewares import ErrorHandlerMiddleWare

from webob import Request,Response
class Application:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        request=Request(environ)
        response=Response()

        response.text="hello world"

  
        return json_response(response.text,start_response)


app = Application()
middleware=ErrorHandlerMiddleWare(
    app=app,
    exception_handler=CommonHandlers.generic_exception_handler
)
