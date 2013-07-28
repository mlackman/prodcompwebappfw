
# TODO: __call__ to handle exceptions like pep333 succests.

import http
import requesthandlers
import services
import re

class WebApp(object):
    """WSGI App"""

    def __init__(self, router, request_factory=None, content_encoder=None): 
        self._router = router
        self._request_factory = request_factory or RequestFactory()
        self._content_encoder = content_encoder or services.ContentEncoder()

    def __call__(self, environ, start_response):
        """WSGI callable"""
        request = self._request_factory.create(environ)
        response = self._router.route(request)
        start_response(response.status, response.headers.items())
        if response.data:
            return [self._encode_response_data(response)]
        else:
            return []

    def _encode_response_data(self, response):
        content_type = response.headers['content-type']
        match = re.search('charset="(?P<encoding>.+)"', content_type)
        if match:
            data = self._content_encoder.encode(response.data, match.group('encoding'))
        else:
            data = response.data
        return data

class Router(object):

    def __init__(self, request_handler_callables):
        """Constructs the request router.
        request_handlers - List of request handler callables. The callable must take http.request
        parameter. It must return tuple containing boolean indicating if the request was served and
        the httpresponse. Example (True, HttpResponse())
        """
        self._request_handlers = request_handler_callables
        # Last handler will respond 404
        self._add_404_request_handler_for_last_request_handler()

    def _add_404_request_handler_for_last_request_handler(self):
        self._request_handlers.insert(len(self._request_handlers), \
            requesthandlers.EveryRequestHandler(http.HttpResponse(http.status.not_found)))

    def route(self, request):
        for request_handler in self._request_handlers:
            served, response = request_handler(request)
            if served: break
        return response

class RequestFactory(object):

    def create(self, environ):
        path = environ['PATH_INFO'] or '/'
        return http.HttpRequest(path, environ['QUERY_STRING'])