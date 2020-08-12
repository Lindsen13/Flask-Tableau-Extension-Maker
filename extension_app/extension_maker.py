from extension_app.db import get_db
import requests
import ast

def execute(extension):
    url = extension['ext_url']
    payload = ast.literal_eval(extension['ext_payload'])
    headers = ast.literal_eval(extension['ext_headers'])
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = str(response.status_code)
        headers = str(response.headers)
    except requests.exceptions.MissingSchema:
        status_code = '-'
        headers = 'invalid url specified. Could not make a HTTP call'
    return {'status_code':status_code,'headers':headers}
    