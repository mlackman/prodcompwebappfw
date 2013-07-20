import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.services import MimeTypeResolver

class TestResolvingMimeTypes(unittest.TestCase):

    def test_mime_type_not_recognised(self):
        resolver = MimeTypeResolver()
        self.assertEquals('text/plain', resolver.get_type('path/to/filename'))

    def test_html_mime_type(self):
        resolver = MimeTypeResolver()
        self.assertEquals('text/html', resolver.get_type('path/to/filename.html'))





if __name__ == '__main__':
    unittest.main()