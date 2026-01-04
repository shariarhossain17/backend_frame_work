from common_handlers import CommonHandlers
from helper import json_response
from middlewares import ErrorHandlerMiddleWare

data ={
      "mobile": [
      {
        "id": "M001",
        "name": "Galaxy S23",
        "brand": "Samsung",
        "price": 799,
        "storage": "128GB",
        "color": "Phantom Black"
      },
      {
        "id": "M002",
        "name": "iPhone 14",
        "brand": "Apple",
        "price": 899,
        "storage": "256GB",
        "color": "Midnight"
      }
    ],
    "camera": [
      {
        "id": "C001",
        "name": "EOS R6",
        "brand": "Canon",
        "price": 2499,
        "type": "Mirrorless",
        "megapixels": 20
      },
      {
        "id": "C002",
        "name": "Alpha 7 IV",
        "brand": "Sony",
        "price": 2799,
        "type": "Mirrorless",
        "megapixels": 33
      }
    ]
}

class Application:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):

        path=environ.get("PATH_INFO","/")
        category=path.split("/")[-1]
        product=data.get(category,[])
  
        return json_response(product,start_response)


app = Application()
middleware=ErrorHandlerMiddleWare(
    app=app,
    exception_handler=CommonHandlers.generic_exception_handler
)
