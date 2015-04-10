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

    def _test_if_else(self):
        tmpl = '{% if a == 1 %}Yes!{% else %}No!{% endif %}'
        self.assertRendered(tmpl, 'Yes!', {'a': 1})
        self.assertRendered(tmpl, 'No!', {'a': 2})
