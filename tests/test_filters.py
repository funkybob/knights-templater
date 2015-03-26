from .utils import TemplateTestCase, Mock


class BasicFilterTest(TemplateTestCase):

    def test_not_filter(self):
        '''Ensure we don't mangle shifts.'''
        self.assertRendered('{{ 8 >> 2 }}', '2')

    def test_basic_filter(self):
        self.assertRendered('{{ foo >> escape }}', 'more &amp; more', {'foo': 'more & more'})

    def test_filter_with_arg(self):
        self.assertRendered('{{ foo >> escape("js") }}', '\\u003Cscript\\u003Eand this\\u003C/script\\u003E', {'foo': '<script>and this</script>'})
