import wsgiref

class HttpStatus(object):

    def __init__(self):
        self.not_found = '404 Not Found'
        self.ok = '200 OK'

status = HttpStatus()


class HttpResponse(object):
    
    def __init__(self, status=None, data=None):
        self.status = status
        self.data = data
        self.headers = wsgiref.headers.Headers([])


class HttpRequest(object):

    def __init__(self, path, query_params=None):
        self.path = path
        self.query_params = query_params or ''

    def query_value(self, query_parameter):
        return 'search words'
