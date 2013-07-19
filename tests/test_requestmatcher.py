import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.requesthandlers import RequestMatcher
from prodcompwebappfw.http import HttpRequest

class TestRequestDoesNotMatch(unittest.TestCase):

    def test_it_does_not_call_handler(self):
        handler = yamf.MockMethod()
        matcher = RequestMatcher('/path', handler)

        handler.mustNotBeCalled

        matcher(HttpRequest('/jee'))

        handler.verify()

class TestRequestMatches(unittest.TestCase):

    def test_it_calls_handler(self):
        handler = yamf.MockMethod()
        matcher = RequestMatcher('/path', handler)

        handler.mustBeCalled

        matcher(HttpRequest('/path'))

        handler.verify()



if __name__ == '__main__':
    unittest.main()
