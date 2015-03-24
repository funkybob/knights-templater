from .utils import TemplateTestCase, Mock


class BasicFilterTest(TemplateTestCase):

    def test_basic_filter(self):
        self.assertRendered('{{ foo >> title }}', 'Bar', {'foo': 'bar'})
