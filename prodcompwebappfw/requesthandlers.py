import re
import os
import http
import services

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
        content_type = ("Content-Type", "text/html")
        return http.HttpResponse(status=http.status.ok, data=content, headers=[content_type])

class StaticFileHandler(object):
    """Reads files from folder and returns the content of the files
    with correct mime type"""

    def __init__(self, filenames, folder, mime_type_resolver=None, filesystem=None):
        """Creates object.
        filenames - list of filenames in folder that are served.
        folder - Folder where the files are loaded"""
        self._filenames = [os.path.join(folder, filename) for filename in filenames]
        self._filesystem = filesystem or services.Filesystem()
        self._mime_type_resolver = mime_type_resolver or services.MimeTypeResolver()

    def __call__(self, request):
        requested_filename = request.path[1:]
        if requested_filename in self._filenames:
            try:
                content = self._filesystem.read(requested_filename)
            except:
                return http.HttpResponse(http.status.not_found)    

            mime_type = self._mime_type_resolver.get_type(requested_filename)
            content_type = ('Content-Type', mime_type)
            return http.HttpResponse(status=http.status.ok, data=content, headers=[content_type])
        else:
            return http.HttpResponse(http.status.not_found)



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
        