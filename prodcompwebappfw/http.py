import wsgiref
import re

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
        self._create_query_params_map(query_params)

    def query_param_value(self, query_parameter):
        """Returns query parameter value by name or None if query parameter does
        not exists"""
        return self.query_params.get(query_parameter, None)

    def _create_query_params_map(self, query_params):
        param_value_pairs = query_params.split('&') if query_params else ''
        self.query_params = {}
        for param_value_pair in param_value_pairs:
            param, value = param_value_pair.split('=')
            self.query_params[param] = value

