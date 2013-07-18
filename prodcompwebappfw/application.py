
# TODO: __call__ to handle exceptions like pep333 succests.
# TODO: start_response must be called

import http
import requesthandlers

class WebApp(object):
    """WSGI App"""

    def __init__(self, router, request_factory=None): 
        self._router = router
        self._request_factory = request_factory

    def __call__(self, environ, start_response):
        """WSGI callable"""
        request = self._request_factory.create(environ)
        self._router.route(request)

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
            requesthandlers.EveryRequestHandler(HttpResponse(http.response.not_found)))

    def route(self, request):
        for request_handler in self._request_handlers:
            served, response = request_handler(request)
            if served: break
        return response

class HttpResponse(object):
    
    def __init__(self, status):
        self.status = status