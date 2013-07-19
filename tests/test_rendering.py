import unittest
import yamf
import sys
from os.path import join, pardir

sys.path.insert(0, join(pardir))
from prodcompwebappfw.renderer import Renderer

class TestRenderer(unittest.TestCase):

    def testRenderingTemplate(self):
        renderer = Renderer('templates')
        self.assertEquals('hello template', renderer.render('hello_template.txt'))

    def testGivingVariables(self):
        renderer = Renderer('templates')
        self.assertEquals('hello jee templates', renderer.render('variables.txt', middle_text='jee'))


if __name__ == '__main__':
    unittest.main()