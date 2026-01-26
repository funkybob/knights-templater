from types import SimpleNamespace

import pytest

from knights import render


class TestLiteralSyntax:
    @pytest.mark.parametrize(
        ('template', 'expected'),
        [
            # plain text
            ('Hello world!', 'Hello world!'),
            # literal literal
            ("{{ 'Hello '}}{{ 'world!' }}", 'Hello world!'),
            # plaintext literal plaintext
            ("Hello {{ 'world' }}!", 'Hello world!'),
            # literal plaintext
            ("{{ 'Hello' }} world!", 'Hello world!'),
            # string literal
            ("{{ 'hello' }}", 'hello'),
            # Numeric literals
            ('{{ 23 }}', '23'),
            ('{{ 2.3 }}', '2.3'),
            ('{{ 12.34 }}', '12.34'),
            ('{{ 12e1 }}', '120.0'),
            ('{{ 12E1 }}', '120.0'),
            ('{{ 12e-1 }}', '1.2'),
            ('{{ 12E-1 }}', '1.2'),
        ],
    )
    def test_render(self, template, expected):
        result = render(template)
        assert result == expected


def f_arg(arg1):
    return f'{arg1}'


def f_args(arg1, arg2):
    return f'{arg1} {arg2}'


class TesteVariableSyntax:
    @pytest.mark.parametrize(
        ('source', 'context', 'expected'),
        [
            # Direct reference
            ('{{ a }}', {'a': 'yes'}, 'yes'),
            # Subscripting
            ('{{ a[1] }}', {'a': ['yes', 'no']}, 'no'),
            ('{{ a["b"] }}', {'a': {'b': 'yes'}}, 'yes'),
            ('{{ a[c] }}', {'a': {'b': 'yes', 'c': 'no'}, 'c': 'b'}, 'yes'),
            # Attribute lookup
            ('{{ a.b }}', {'a': SimpleNamespace(b=1)}, '1'),
            ('{{ a.b.c }}', {'a': SimpleNamespace(b=SimpleNamespace(c=1))}, '1'),
            ('{{ a["b"].c }}', {'a': {'b': SimpleNamespace(c=1)}}, '1'),
        ],
    )
    def test_direct(self, source, context, expected):
        result = render(source, context)
        assert result == expected

    @pytest.mark.parametrize(
        ('source', 'context', 'expected'),
        [
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
        ],
    )
    def test_function(self, source, context, expected):
        result = render(source, context)
        assert result == expected

    def test_builtin(self):
        result = render('{{ ", ".join(map(str, [1,2,3,4])) }}')
        assert result == '1, 2, 3, 4'
