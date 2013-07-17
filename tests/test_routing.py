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
        router.route.mustBeCalled.withArgs(request)

        app(environ, yamf.MockMethod())

        router.verify()
        request_factory.verify()

class TestRouteNotFound(unittest.TestCase):

    def test_it_returns_404(self):
        router = Router([])
        response = router.route(None)
        self.assertEquals(response.status, http.response.not_found)


if __name__ == '__main__':
    unittest.main()

