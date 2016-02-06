
import pathlib

from .utils import TemplateTestCase


class InheritanceTestCase(TemplateTestCase):

    def test_simple(self):
        '''
        Test that we can inherit.
        '''
        t = self.loader.load('inherit_simple.html')
        output = t({})
        self.assertEqual(output, 'parent\n\n')

    def test_override_block(self):
        t = self.loader.load('inherit_override.html')
        output = t({})
        self.assertEqual(output, 'parent\nchild\n')


class SuperTestCase(TemplateTestCase):

    def test_own_super(self):
        t = self.loader.load('super_own.html')
        output = t({})
        self.assertEqual(output, 'child of parent\nother parent\n')

    def test_other_super(self):
        t = self.loader.load('super_other.html')
        output = t({})
        self.assertEqual(output, 'subverting other parent\nother parent\n')
