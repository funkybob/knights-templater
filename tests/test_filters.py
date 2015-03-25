from .utils import TemplateTestCase, Mock


class BasicFilterTest(TemplateTestCase):

    def test_not_filter(self):
        '''Ensure we don't mangle shifts.'''
        self.assertRendered('{{ 8 >> 2 }}', '2')

    def test_basic_filter(self):
        self.assertRendered('{{ foo >> title }}', 'Bar', {'foo': 'bar'})

    def test_filter_with_arg(self):
        self.assertRendered('{{ foo >> add("more") }}', 'barmore', {'foo': 'bar'})
