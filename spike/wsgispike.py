import urlparse
import wsgiref
from jinja2 import Environment, FileSystemLoader
from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    """Simplest possible application object"""
    print environ['PATH_INFO']
    print urlparse.urlparse(wsgiref.util.request_uri(environ))
    env = Environment(loader=FileSystemLoader('templates'))
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)

    response = env.get_template('index.html').render()
    return [response.encode('utf-8')]

# Instantiate the WSGI server.
# It will receive the request, pass it to the application
# and send the application's response to the client
httpd = make_server(
   'localhost', # The host name.
   8051, # A port number where to wait for the request.
   simple_app # Our application object name, in this case a function.
   )

httpd.serve_forever()