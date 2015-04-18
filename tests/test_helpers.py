
from .utils import TemplateTestCase


class HelpersTestCase(TemplateTestCase):

    def test_escape_html(self):
        self.assertRendered(
            '''{{ _.escape("foo & bar") }}''',
            '''foo &amp; bar''',
            {},
        )

    def test_escape_js(self):
        self.assertRendered(
            '''{{ _.escape('=', 'js') }}''',
            '''\\u003D''',
            {},
        )
