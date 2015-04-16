
import os.path

from .utils import TemplateTestCase

from knights import loader


loader.add_path(os.path.join(os.path.dirname(__file__), 'templates/'))


class InheritanceTestCase(TemplateTestCase):

    def test_simple(self):
        '''
        Test that we can inherit.
        '''
        t = loader.load_template('inherit_simple.html')
        output = t({})
        self.assertEqual(output, 'parent\n\n')

    def test_override_block(self):
        t = loader.load_template('inherit_override.html')
        output = t({})
        self.assertEqual(output, 'parent\nchild\n')
