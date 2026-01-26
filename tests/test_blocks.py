from types import SimpleNamespace

import pytest

from knights import render


class TestBlockTag:
    def test_parse(self):
        result = render('{% block name %}%{% endblock %}')
        assert result == '%'


class TestForTag:
    @pytest.mark.parametrize(
        ('source', 'expected', 'context'),
        [
            # Simple for block
            (
                '{% for item in seq %}{{ item }} {% endfor %}',
                'a b c d e ',
                {'seq': 'abcde'},
            ),
            # Unpack item
            (
                '{% for a, b in seq %}{{ a }} == {{ b }},{% endfor %}',
                'a == 1,b == 2,',
                {'seq': (('a', 1), ('b', 2))},
            ),
            # Ignore empty block
            (
                '{% for a, b in seq %}{{ a }} == {{ b }},{% empty %}empty{% endfor %}',
                'a == 1,b == 2,',
                {'seq': (('a', 1), ('b', 2))},
            ),
            # Renders empty block
            (
                '{% for a, b in seq %}{{ a }} == {{ b }},{% empty %}empty{% endfor %}',
                'empty',
                {'seq': ()},
            ),
            # Scope climbing
            (
                '{% for a in seq %}{{ a * b }} {% endfor %}',
                '2 4 6 ',
                {'seq': (1, 2, 3), 'b': 2},
            ),
            # Attribute lookup on source
            (
                '{% for a in obj.seq %}{{ a }}{% endfor %}',
                '1234',
                {'obj': SimpleNamespace(seq=[1, 2, 3, 4])},
            ),
        ],
    )
    def test_for_tag(self, source, expected, context):
        result = render(source, context)
        assert result == expected


class TestIfTag:
    @pytest.mark.parametrize(
        ('context', 'expected'),
        [
            ({'a': 1}, 'Yes!'),
            ({'a': 2}, ''),
        ],
    )
    def test_simple_if_true(self, context, expected):
        result = render('{% if a == 1 %}Yes!{% endif %}', context)
        assert result == expected

    @pytest.mark.parametrize(
        ('context', 'expected'),
        [
            ({'a': 1}, 'Yes!'),
            ({'a': 2}, 'No!'),
        ],
    )
    def test_if_else(self, context, expected):
        result = render('{% if a == 1 %}Yes!{% else %}No!{% endif %}', context)
        assert result == expected


class TestWithTag:
    def test_simple_with(self):
        result = render('{% with a=1, b=c %}{{ a * b }}{% endwith %}', {'c': 3})
        assert result == '3'


class TestIncludeTag:
    def test_include(self, test_loader):
        result = render("""{% include "include.html" %}""", loader=test_loader)
        assert result == 'included\n'

    def test_include_with(self, test_loader):
        result = render("""{% include "include_more.html", a=val, b=6 %}""", {'val': 3}, loader=test_loader)
        assert result == 'product: 18\n'


class TestMacroTagTest:
    def test_macro_does_not_render(self):
        result = render("""{% macro foo %}Foo{% endmacro %}""")
        assert result == ''

    def test_macro_renders(self):
        result = render("""{% macro foo %}Foo{% endmacro %}{% use "foo" %}""")
        assert result == 'Foo'

    def test_macro_takes_args(self):
        result = render("""{% macro foo %}{{ foo }}{% endmacro %}{% use "foo", foo="bar" %}""")
        assert result == """bar"""
