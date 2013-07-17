from wsgiref.simple_server import make_server

class ProductCompareWebApp(object):

    def __init__(self, index_template, products_template, no_products_found_template, \
                 error_template, databases):
        """Creates web app.
        index_template - Location of the jinja2 template for the index page.
        products_template - Location of the jinja2 template for the page, which shows the found products
        databases - Location of the databases"""
        pass
        
    def serve_once(self, port):
        """Helper method to serve this app on localhost"""
        print 'serving'
        httpd = make_server('localhost', port, self)
        httpd.handle_request()
        print 'out'

    def __call__(self, environ, start_response):
        response_headers = [('Content-type', 'text/html')]
        start_response('200 OK', response_headers)
        return ['']