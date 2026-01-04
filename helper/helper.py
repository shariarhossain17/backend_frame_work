import json


def json_response(response:dict | list[dict],start_response,status="200 OK", response_headers=[])->list[bytes]:
    response_body=json.dumps(response)
    response_headers.append((
        'Content-type', 'text/json'
    ))
    start_response(status,response_headers)
    return [response_body.encode('utf-8')]