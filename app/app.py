from helper import json_response


class Application:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
  
        return json_response("hello thik hai",start_response)


app = Application()
