import re
import http

"""
RequestHandler objects must implement serve method, which returns tuple (request_served, 
    httpresponse or None)."""

class EveryRequestHandler(object):
    """Serves any request asked to be served with given
    response"""

    def __init__(self, response):
        self._response = response

    def __call__(self, request):
        "Serves all requests with given response"
        return True, self._response

class StaticPageHandler(object):

    def __init__(self, renderer, template_name):
        self._renderer = renderer
        self._template_name = template_name

    def __call__(self, request):
        content = self._renderer.render(self._template_name)
        return http.HttpResponse(status=http.status.ok, data=content)

class RequestMatcher(object):
    """Object to match url and if the url matches then calls the handler callable"""

    def __init__(self, url_regexp, handler_callable):
        self._regexp = re.compile(url_regexp)
        self._handler_callable = handler_callable

    def __call__(self, request):
        if self._regexp.match(request.path):
            return True, self._handler_callable(request)
        else:
            return False, None
        