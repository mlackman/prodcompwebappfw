import unittest
import sys
import threading
import urllib2
from bs4 import BeautifulSoup
import time

from os.path import pardir,join
sys.path.insert(0, join(pardir, pardir))

from prodcompwebappfw import ProductCompareWebApp

class TestServingPages(unittest.TestCase):

    def test_serving_index_page(self):
        self.app = ProductCompareWebApp(index_template='templates/index.html',\
                                        products_template='templates/products.html',\
                                        no_products_found_template='templates/no_products.html',
                                        error_template='templates/error.html',
                                        databases = ['database'])
        webAppServeThread = threading.Thread(target=self.execute)
        webAppServeThread.start()
        time.sleep(1)
        f = urllib2.urlopen('http://localhost:8085')
        html = f.read()
        f.close()

        soup = BeautifulSoup(html)

        self.assertEquals(soup.title, 'index_page')

    def execute(self):
        self.app.serve_once(8085)

if __name__ == '__main__':
    unittest.main()
 
    

