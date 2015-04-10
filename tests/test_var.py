from .utils import TemplateTestCase, Mock


class LiteralSyntaxTest(TemplateTestCase):

    def test_render_plaintext(self):
        self.assertRendered("Hello world!", 'Hello world!')

    def test_render_plaintext_literal_literal(self):
        self.assertRendered("{{ 'Hello '}}{{ 'world!' }}", 'Hello world!')

    def test_render_plaintext_literal_plaintext(self):
        self.assertRendered("Hello {{ 'world' }}!", 'Hello world!')

    def test_render_literal_plaintext(self):
        self.assertRendered("{{ 'Hello' }} world!", 'Hello world!')

    def test_renderStringLiteral(self):
        self.assertRendered("{{ 'hello' }}", 'hello')

    def test_renderNumLiteral(self):
        # A list of (template, context, output)
        TESTS = (
            ('{{ 23 }}', '23'),

            ('{{ 2.3 }}', '2.3'),
            ('{{ 12.34 }}', '12.34'),
            ('{{ 12e1 }}', '120.0'),
            ('{{ 12E1 }}', '120.0'),
            ('{{ 12e-1 }}', '1.2'),
            ('{{ 12E-1 }}', '1.2'),
        )
        for src, expect in TESTS:
            self.assertRendered(src, expect)


class VariableSyntaxTest(TemplateTestCase):

    def test_direct(self):
        # A list of (template, context, output)
        TESTS = (
            ('{{ a }}', {'a': 'yes'}, 'yes'),
        )
        for src, ctx, expect in TESTS:
            self.assertRendered(src, expect, ctx)

    def test_index(self):
        # A list of (template, context, output)
        TESTS = (
            ('{{ a[1] }}', {'a': ['yes', 'no']}, 'no'),
            ('{{ a["b"] }}', {'a': {'b': 'yes'}}, 'yes'),
            ('{{ a[c] }}', {'a': {'b': 'yes', 'c': 'no'}, 'c': 'b'}, 'yes'),
        )
        for src, ctx, expect in TESTS:
            self.assertRendered(src, expect, ctx)

    def test_attribute(self):
        # A list of (template, context, output)
        TESTS = (
            ('{{ a.b }}', {'a': Mock(b=1)}, '1'),
            ('{{ a.b.c }}', {'a': Mock(b=Mock(c=1))}, '1'),
            ('{{ a["b"].c }}', {'a': {'b': Mock(c=1)}}, '1'),
        )
        for src, ctx, expect in TESTS:
            self.assertRendered(src, expect, ctx)

    def test_function(self):

        def f_arg(arg1):
            return '%s' % (arg1)

        def f_args(arg1, arg2):
            return '%s %s' % (arg1, arg2)

        # A list of (template, context, output)
        TESTS = (
            ('{{ a(1) }}', {'a': lambda x: x}, '1'),
            ('{{ a(b,1) }}', {'a': lambda x, y: x + y, 'b': 6}, '7'),

            # args
            ('{{ a(1) }}', {'a': f_arg}, '1'),
            ('{{ a(1, 2) }}', {'a': f_args}, '1 2'),

            # kwargs
            ('{{ a(arg1=1) }}', {'a': f_arg}, '1'),
            ('{{ a(arg1=1, arg2=2) }}', {'a': f_args}, '1 2'),

            # args + kwargs
            ('{{ a(1, arg2=2) }}', {'a': f_args}, '1 2'),

            # with vars
            ('{{ a(x) }}', {'a': f_arg, 'x': 1}, '1'),
            ('{{ a(x, y) }}', {'a': f_args, 'x': 1, 'y': 2}, '1 2'),
            ('{{ a(arg1=x) }}', {'a': f_arg, 'x': 1}, '1'),
            ('{{ a(arg1=x, arg2=y) }}', {'a': f_args, 'x': 1, 'y': 2}, '1 2'),
            ('{{ a(x, arg2=y) }}', {'a': f_args, 'x': 1, 'y': 2}, '1 2'),
        )
        for src, ctx, expect in TESTS:
            self.assertRendered(src, expect, ctx)
