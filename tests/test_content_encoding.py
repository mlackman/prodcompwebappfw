import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.application import WebApp, Router, RequestFactory
from prodcompwebappfw import http

class TestWebAppEncodesContentAccordingToContentTypeWebHeader(unittest.TestCase):

    def setUp(self):
        self.request_factory = yamf.Mock()
        self.router = yamf.Mock()
        self.content_encoder = yamf.Mock()
        self.app = WebApp(self.router, self.request_factory, self.content_encoder)

    def test_encoding_to_utf8(self):
        response = http.HttpResponse(data='data to be encoded')
        response.headers.add_header('content-type','text/html', charset='utf8')
        self.router.route.returns(response)

        self.content_encoder.encode.mustBeCalled.withArgs('data to be encoded', 'utf8')

        self.app({}, yamf.MockMethod())

        self.content_encoder.verify()

    def test_encoding_to_ISO88591(self):
        response = http.HttpResponse(data='data to be encoded')
        response.headers.add_header('content-type','text/html', charset='ISO-8859-1')
        self.router.route.returns(response)

        self.content_encoder.encode.mustBeCalled.withArgs('data to be encoded', 'ISO-8859-1')

        self.app({}, yamf.MockMethod())

        self.content_encoder.verify()

    def test_encoding_not_done_if_charset_not_defined(self):
        response = http.HttpResponse(data='data to be encoded')
        response.headers.add_header('content-type','text/html')
        self.router.route.returns(response)

        self.content_encoder.encode.mustNotBeCalled
        
        self.app({}, yamf.MockMethod())

        self.content_encoder.verify()

if __name__ == '__main__':
    unittest.main()