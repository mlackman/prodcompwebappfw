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
        response = http.HttpResponse(http.status.ok, content)
        response.headers.add_header('Content-Type', 'text/html', charset='utf8')
        return response

class StaticFileHandler(object):
    """Reads files from folder and returns the content of the files
    with correct mime type"""

    def __init__(self, filenames, folder, filesystem=None):
        """Creates object.
        filenames - list of filenames in folder that are served.
        folder - Folder where the files are loaded"""
        self._filenames = [os.path.join(folder, filename) for filename in filenames]
        self._filesystem = filesystem or services.Filesystem()
        self._mime_type_resolver = services.MimeTypeResolver()

    def __call__(self, request):
        requested_filename = request.path[1:]
        if requested_filename in self._filenames:
            try:
                content = self._filesystem.read(requested_filename)
            except:
                return http.HttpResponse(http.status.not_found)    

            
            response = http.HttpResponse(status=http.status.ok, data=content)
            self._set_headers(response, requested_filename)
            return response
        else:
            return http.HttpResponse(http.status.not_found)

    def _set_headers(self, response, requested_filename):
        mime_type = self._mime_type_resolver.get_type(requested_filename)
        if mime_type.is_text_type:
            response.headers.add_header('Content-Type', str(mime_type), charset='utf8')
        else:
            response.headers.add_header('Content-Type', str(mime_type))



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
        