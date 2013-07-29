import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.requesthandlers import SearchProductsHandler
from prodcompwebappfw import http, renderer
import productrepository

class TestNoProductsFound(unittest.TestCase):

    def setUp(self):
        self.renderer = yamf.Mock(renderer.Renderer)
        self.database = yamf.Mock(productrepository.ProductRepository)
        self.database.search.mustBeCalled.withArgs('search words')\
                     .returns(productrepository.SearchResult())
        self.handler = SearchProductsHandler(no_products_template='no_products.html',\
                                             products_template='products.html',\
                                             database=self.database,\
                                             renderer=self.renderer)

    def test_it_searches_database_with_query_parameter(self):
        self.handler(http.HttpRequest(path='/search', query_params='q=search words'))

        self.database.verify()

    def test_it_renders_no_products_template_when_no_hits_found(self):
        self.renderer.render.mustBeCalled.withArgs('no_products.html')
        self.handler(http.HttpRequest(path='/search', query_params='q=search words'))
        self.renderer.verify()

    def test_it_puts_renderered_data_to_response(self):
        self.renderer.render.returns('rendered data')
        response = self.handler(http.HttpRequest(path='/search', query_params='q=search words'))
        self.assertEquals('rendered data', response.data)

class TestProductsFound(unittest.TestCase):

    def setUp(self):
        self.renderer = yamf.Mock(renderer.Renderer)
        self.database = yamf.Mock(productrepository.ProductRepository)
        self.handler = SearchProductsHandler(no_products_template='no_products.html',\
                                             products_template='products.html',\
                                             database=self.database,\
                                             renderer=self.renderer)

    def test_it_renders_products_template_when_hits_found(self):
        result = productrepository.SearchResult()
        result.products = [yamf.Mock()]
        result.page_count = 1
        self.database.search.returns(result)

        self.renderer.render.mustBeCalled.withArgs('products.html', products=result.products, \
            search_words = 'search words')
        self.handler(http.HttpRequest(path='/search', query_params='q=search words'))
        self.renderer.verify()


if __name__ == '__main__':
    unittest.main()
