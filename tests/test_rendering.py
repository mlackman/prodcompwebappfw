import unittest
import yamf
import sys
from os.path import join, pardir, abspath, dirname

sys.path.insert(0, join(pardir))
from prodcompwebappfw.renderer import Renderer

class TestRenderer(unittest.TestCase):

    def setUp(self):
        self.renderer = Renderer(join(dirname(abspath(__file__)), 'templates'))

    def testRenderingTemplate(self):
        self.assertEquals('hello template', \
            self.renderer.render('hello_template.txt'))

    def testGivingVariables(self):
        self.assertEquals('hello jee templates', \
            self.renderer.render('variables.txt', middle_text='jee'))


if __name__ == '__main__':
    unittest.main()