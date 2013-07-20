import os
from wsgiref.simple_server import make_server
import application
import requesthandlers
import renderer

print dir()
def create_app():
    pass

class ProductCompareWebApp(object):

    def __init__(self, template_folder, index_template, products_template, no_products_found_template, \
                 error_template, static_content_folder, databases):
        """Creates web app.
        template_folder - Path to the templates
        index_template - Index page template name
        products_template - ...
        databases - Location of the databases"""
        indexHandler = requesthandlers.StaticPageHandler(renderer.Renderer(template_folder),\
                                                         index_template)
        matcher = requesthandlers.RequestMatcher('^/$', indexHandler)

        static_file_handler = requesthandlers.StaticFileHandler(os.listdir(static_content_folder),\
                                                                static_content_folder)
        static_file_matcher = requesthandlers.RequestMatcher('^/' + static_content_folder + '/.*',
                                                             static_file_handler)

        self._routes = application.Router([matcher, static_file_matcher])
        
    def serve_once(self, port):
        """Helper method to serve this app on localhost"""
        httpd = make_server('localhost', port, self)
        httpd.handle_request()

    def serve(self, port=None):
        httpd = make_server('localhost', port or 8085, self)
        httpd.serve_forever()

    def __call__(self, environ, start_response):
        app = application.WebApp(self._routes)
        return app(environ, start_response)