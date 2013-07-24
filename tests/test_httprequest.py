import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.http import HttpRequest

class TestQueryParams(unittest.TestCase):

    def test_no_query_params(self):
        request = HttpRequest('', '')
        self.assertEquals(request.query_param_value('parameter'), None)

    def test_single_query_param(self):
        request = HttpRequest('', 'param=5')
        self.assertEquals(request.query_param_value('param'), '5')

    def test_three_query_params(self):
        request = HttpRequest('', 'param=5&other_param=word&variable=a')
        self.assertEquals(request.query_param_value('other_param'), 'word')



if __name__ == '__main__':
    unittest.main()