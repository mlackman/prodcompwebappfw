import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.requesthandlers import SearchProductsHandler
from prodcompwebappfw import http
import productrepository

class TestSearchProductsHandler(unittest.TestCase):

    def test_it_searches_database_with_query_parameter(self):
        database = yamf.Mock(productrepository.ProductRepository)
        database.search.mustBeCalled.withArgs('search words').returns(productrepository.SearchResult())
        handler = SearchProductsHandler(database)

        handler(http.HttpRequest(path='/search', query_params='q=search words'))

        database.verify()


if __name__ == '__init__':
    unittest.main()
