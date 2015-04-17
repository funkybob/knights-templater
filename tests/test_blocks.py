import os

from .utils import TemplateTestCase


class BlockTagTest(TemplateTestCase):

    def test_block_parse(self):
        self.assertRendered('{% block name %}%{% endblock %}', '%')


class ForTagTest(TemplateTestCase):
    def test_simple_for(self):
        self.assertRendered(
            '{% for item in seq %}{{ item }} {% endfor %}',
            'a b c d e ',
            {'seq': 'abcde'},
        )

    def test_unpack_for(self):
        self.assertRendered(
            '{% for a, b in seq %}{{ a }} == {{ b }},{% endfor %}',
            'a == 1,b == 2,',
            {'seq': (('a', 1), ('b', 2))}
        )

    def test_for_empty_false(self):
        self.assertRendered(
            '{% for a, b in seq %}{{ a }} == {{ b }},{% empty %}empty{% endfor %}',
            'a == 1,b == 2,',
            {'seq': (('a', 1), ('b', 2))},
        )

    def test_for_empty_true(self):
        self.assertRendered(
            '{% for a, b in seq %}{{ a }} == {{ b }},{% empty %}empty{% endfor %}',
            'empty',
            {'seq': (),},
        )

    def test_scope(self):
        self.assertRendered(
            '{% for a in seq %}{{ a * b }} {% endfor %}',
            '2 4 6 ',
            {'seq': (1, 2, 3), 'b': 2},
        )

class IfTagTest(TemplateTestCase):
    def test_simple_if(self):
        self.assertRendered(
            '{% if a == 1 %}Yes!{% endif %}',
            'Yes!',
            {'a': 1}
        )

        self.assertRendered(
            '{% if a == 1 %}Yes!{% endif %}',
            '',
            {'a': 2}
        )

    def test_if_else(self):
        tmpl = '{% if a == 1 %}Yes!{% else %}No!{% endif %}'
        self.assertRendered(tmpl, 'Yes!', {'a': 1})
        self.assertRendered(tmpl, 'No!', {'a': 2})


class WithTagTest(TemplateTestCase):
    def test_simple_with(self):
        self.assertRendered(
            '''{% with a=1, b=c %}{{ a * b }}{% endwith %}''',
            '''3''',
            {'c': 3}
        )


class IncludeTagTest(TemplateTestCase):
    def setUp(self):
        from knights import loader
        loader.add_path(os.path.join(os.path.dirname(__file__), 'templates/'))

    def test_include(self):
        self.assertRendered(
            '''{% include "include.html" %}''',
            '''included\n''',
            {}
        )

    def test_include_with(self):
        self.assertRendered(
            '''{% include "include_more.html", a=val, b=6 %}''',
            '''product: 18\n''',
            {'val': 3}
        )
