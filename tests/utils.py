import pathlib
import unittest


from knights import compiler, loader


class Mock(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TemplateTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = loader.TemplateLoader([
            pathlib.Path(__file__).parent / 'templates',
        ])

    def assertRendered(self, source, expected, context=None):
        try:
            tmpl = compiler.kompile(source, loader=self.loader)
            rendered = tmpl({} if context is None else context)
            self.assertEqual(rendered, expected)
        except Exception as e:
            if hasattr(e, 'message'):
                standardMsg = e.message
            elif hasattr(e, 'args') and len(e.args) > 0:
                standardMsg = e.args[0]
            else:
                standardMsg = ''
            msg = 'Failed rendering template %s:\n%s: %s' % (
                source, e.__class__.__name__, standardMsg)
            self.fail(msg)
