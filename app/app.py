from common_handlers import CommonHandlers
from helper import json_response
from middlewares import ErrorHandlerMiddleWare


class Application:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
  
        return json_response("hello thik hai",start_response)


app = Application()
middleware=ErrorHandlerMiddleWare(
    app=app,
    exception_handler=CommonHandlers.generic_exception_handler
)
