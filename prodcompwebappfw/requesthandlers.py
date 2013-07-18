
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
