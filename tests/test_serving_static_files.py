import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.requesthandlers import StaticFileHandler
from prodcompwebappfw import http

class TestFileNotFound(unittest.TestCase):

    def test_it_returns_404_when_filename_not_specified(self):
        filesystem = yamf.Mock()
        handler = StaticFileHandler([], 'static', filesystem)
        response = handler(http.HttpRequest('/static/somefile.css'))

        self.assertEquals(response.status, http.status.not_found)

    def test_it_returns_404_when_file_cannot_be_read(self):
        filesystem = yamf.Mock()
        handler = StaticFileHandler(['somefile.css'], 'static', filesystem)
        def raiseError(self): raise Exception()
        filesystem.read.execute(raiseError)

        response = handler(http.HttpRequest('/static/somefile.css'))

        self.assertEquals(response.status, http.status.not_found)

class TestFileFound(unittest.TestCase):

    def test_css_file_is_returned(self):
        filesystem = yamf.Mock()
        filesystem.read.returns('content')
        handler = StaticFileHandler(['somefile.css'], 'static', filesystem)
        response = handler(http.HttpRequest('/static/somefile.css'))

        self.assertEquals(response.status, http.status.ok)
        self.assertEquals(response.data, 'content')
        self.assertTrue(('Content-Type', 'text/css') in response.headers)






if __name__ == '__main__':
    unittest.main()