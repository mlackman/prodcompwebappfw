import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.application import WebApp, Router, RequestFactory
from prodcompwebappfw import http

"""
Routing is handled by WebApp and Router. WebApp is responsible for 
creating Request object from http request and asking Router to route the request
"""

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.request_factory = yamf.Mock()
        self.router = yamf.Mock()
        self.app = WebApp(self.router, self.request_factory)

    def test_it_routes_requests(self):
        environ = {}
        request = yamf.Mock()
        self.request_factory.create.mustBeCalled.withArgs(environ).returns(request)
        self.router.route.mustBeCalled.withArgs(request).returns(http.HttpResponse())

        self.app(environ, yamf.MockMethod())

        self.router.verify()
        self.request_factory.verify()

    def test_it_responses(self):
        response = http.HttpResponse(status="100 this is the text", data="data")
        response.headers.add_header('content-type','text/html')
        self.router.route.returns(response)

        start_response = yamf.MockMethod()
        start_response.mustBeCalled.withArgs("100 this is the text", 
            [('content-type', 'text/html')])

        environ = {}
        self.assertEquals(self.app(environ, start_response), ["data"])
        start_response.verify()


class TestRouteNotFound(unittest.TestCase):

    def test_it_returns_404(self):
        request_handler = yamf.MockMethod()
        request_handler.returns((False, None))
        router = Router([request_handler])
        response = router.route(None)
        self.assertEquals(response.status, http.status.not_found)

class TestRouteFound(unittest.TestCase):
    
    def test_it_returns_response_from_callable(self):
        request_handler = yamf.MockMethod()
        request_handler.returns((True, 1))
        router = Router([request_handler])

        self.assertEquals(1, router.route(None))

    def test_it_returns_response_from_first_serving_callable(self):
        request_handler = yamf.MockMethod()
        request_handler.returns((False, None))
        router = Router([self.create_request_handler_mock((False, 0)),
                         self.create_request_handler_mock((True, 1)),
                         self.create_request_handler_mock((True, 2))])

        self.assertEquals(1, router.route(None))

    def create_request_handler_mock(self, return_value):
        request_handler = yamf.MockMethod()
        request_handler.returns(return_value)
        return request_handler

class TestCreatingRequests(unittest.TestCase):

    def setUp(self):
        self.environ = {'QUERY_STRING':''}

    def testEmptyPath(self):
        self.environ['PATH_INFO'] = ''
        f = RequestFactory()
        request = f.create(self.environ)
        self.assertEquals(request.path, '/')

    def testComplesPath(self):
        self.environ['PATH_INFO'] = '/data/path?q=jee&j=q'
        f = RequestFactory()
        request = f.create(self.environ)
        self.assertEquals(request.path, '/data/path?q=jee&j=q')


if __name__ == '__main__':
    unittest.main()

