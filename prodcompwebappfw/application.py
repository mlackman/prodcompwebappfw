
# TODO: __call__ to handle exceptions like pep333 succests.
# TODO: start_response must be called

import http

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

    def __init__(self, routes):
        pass

    def route(self, request):
        return HttpResponse(http.response.not_found)

class HttpResponse(object):
    
    def __init__(self, status):
        self.status = status