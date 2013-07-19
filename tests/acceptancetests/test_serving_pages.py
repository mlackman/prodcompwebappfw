import unittest
import sys
import threading
import urllib2
from bs4 import BeautifulSoup
import time

from os.path import pardir,join, abspath, dirname
sys.path.insert(0, join(pardir, pardir))

from prodcompwebappfw import ProductCompareWebApp

class TestServingPages(unittest.TestCase):

    def setUp(self):
        self.app = ProductCompareWebApp(template_folder = join(dirname(abspath(__file__)),'templates'),
                                        index_template='index.html',\
                                        products_template='products.html',\
                                        no_products_found_template='no_products.html',
                                        error_template='error.html',
                                        static_content_folder='static',
                                        databases = ['database'])

    def test_serving_index_page(self):
        webAppServeThread = threading.Thread(target=self.execute)
        webAppServeThread.start()
        time.sleep(1)
        f = urllib2.urlopen('http://localhost:8085')
        html = f.read()
        f.close()

        soup = BeautifulSoup(html)

        self.assertEquals(soup.title.string, 'index_page')

    def test_serving_static_content(self):
        webAppServeThread = threading.Thread(target=self.execute)
        webAppServeThread.start()
        time.sleep(1)
        f = urllib2.urlopen('http://localhost:8085/static/main.css')
        css = f.read()
        f.close()

        self.assertEquals(css, 'css file')

    def execute(self):
        self.app.serve_once(8085)

if __name__ == '__main__':
    unittest.main()
 
    

