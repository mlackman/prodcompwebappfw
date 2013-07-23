import unittest
import sys
import threading
import urllib2
from bs4 import BeautifulSoup
import time
import yamf
import productrepository

from os.path import pardir,join, abspath, dirname
sys.path.insert(0, join(pardir, pardir))

from prodcompwebappfw import ProductCompareWebApp

class TestServingPages(unittest.TestCase):

    def setUp(self):
        self.database = yamf.Mock(productrepository.ProductRepository)
        self.app = ProductCompareWebApp(template_folder = join(dirname(abspath(__file__)),'templates'),
                                        index_template='index.html',\
                                        products_template='products.html',\
                                        no_products_found_template='no_products.html',
                                        error_template='error.html',
                                        static_content_folder='static',
                                        databases = ['database'],
                                        database=self.database)

    def test_serving_index_page(self):
        self.start_server()
        html = self.read('http://localhost:8085')

        soup = BeautifulSoup(html)

        self.assertEquals(soup.title.string, 'index_page')

    def test_serving_static_content(self):
        self.start_server()
        css = self.read('http://localhost:8085/static/main.css')
        self.assertEquals(css, 'css file')

    def test_showing_products(self):
        self.start_server()

        product = productrepository.Product('Saha', 'url', 'image_url', 'description', 'price')
        result = productrepository.SearchResult()
        result.page_count = 1
        result.products = [product]
        self.database.search.returns(result)

        html = self.read('http://localhost:8085/search?q=vene')

        soup = BeautifulSoup(html)
        self.assertEquals(soup.find_all('div', class_='product-info'), 1)
        
    def read(self, url):
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
        return data

    def start_server(self):
        webAppServeThread = threading.Thread(target=self.execute)
        webAppServeThread.start()
        time.sleep(1)

    def execute(self):
        self.app.serve_once(8085)

if __name__ == '__main__':
    unittest.main()
 
    

