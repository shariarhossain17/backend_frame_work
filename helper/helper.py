import json

def json_response(response, start_response, status="200 OK", response_headers=None):
    if response_headers is None:
        response_headers = []

    # Convert Response-like objects or any custom object to a string
    if not isinstance(response, (dict, list)):
        response = {"message": str(response)}

    response_body = json.dumps(response)
    response_headers.append(('Content-Type', 'text/json'))
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]
