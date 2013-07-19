from wsgiref.simple_server import make_server
import application
import requesthandlers
import renderer

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
        matcher = requesthandlers.RequestMatcher('/$', indexHandler)
        self._routes = application.Router([matcher])
        
    def serve_once(self, port):
        """Helper method to serve this app on localhost"""
        httpd = make_server('localhost', port, self)
        httpd.handle_request()

    def __call__(self, environ, start_response):
        app = application.WebApp(self._routes)
        return app(environ, start_response)