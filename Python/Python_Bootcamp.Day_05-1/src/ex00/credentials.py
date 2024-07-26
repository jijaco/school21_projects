from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import json


def application(environ, start_response):
    request_method = environ['REQUEST_METHOD']
    query = parse_qs(environ['QUERY_STRING'])
    species = query.get('species', 'Error')
    response_body = {'Cyberman': 'John Lumic',
                     'Dalek': 'Davros',
                     'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
                     'Human': 'Leonardo da Vinci',
                     'Ood': 'Klineman Halpen',
                     'Silence': 'Tasha Lem',
                     'Slitheen': 'Coca-Cola salesman',
                     'Sontaran': 'General Staal',
                     'Time Lord': 'Rassilon',
                     'Weeping Angel': 'The Division Representative',
                     'Zygon': 'Broton'}
    status = '200 OK'
    if request_method == 'GET':
        if species == 'Error':
            response_body = species
            status = '400 Bad Request'
        else:
            if response_body.get(species[0], 'Unknown') == 'Unknown':
                status = '404 Not Found'
            response_body = json.dumps(
                {'credentials': response_body.get(species[0], 'Unknown')})
    else:
        response_body = species
        status = '400 Bad Request'

    response_headers = [('Content-Type', 'text/plain')]
    print(response_body)
    start_response(status, response_headers)
    return [str.encode(response_body)]


httpd = make_server('localhost', 8888, application)

httpd.serve_forever()
