import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.application import WebApp, Router
from prodcompwebappfw import http

"""
Routing is handled by WebApp and Router. WebApp is responsible for 
creating Request object from http request and asking Router to route the request
"""

class TestWebApp(unittest.TestCase):

    def test_it_routes_requests(self):
        request_factory = yamf.Mock()
        router = yamf.Mock()
        app = WebApp(router, request_factory)

        environ = {}
        request = yamf.Mock()
        request_factory.create.mustBeCalled.withArgs(environ).returns(request)
        router.route.mustBeCalled.withArgs(request).returns(http.HttpResponse())

        app(environ, yamf.MockMethod())

        router.verify()
        request_factory.verify()

    def test_it_responses(self):
        request_factory = yamf.Mock()
        router = yamf.Mock()
        app = WebApp(router, request_factory)
        
        router.route.returns(http.HttpResponse(status="100 this is the text", data="data", 
                                                    headers=['jee']))
        start_response = yamf.MockMethod()
        start_response.mustBeCalled.withArgs("100 this is the text", ['jee'])

        environ = {}
        self.assertEquals(app(environ, start_response), "data")
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



if __name__ == '__main__':
    unittest.main()

