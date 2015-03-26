from .utils import TemplateTestCase, Mock


class BlockTagTest(TemplateTestCase):

    def test_block_parse(self):
        self.assertRendered('{% now "%%" %}', '%')


class ForTagTest(TemplateTestCase):
    def test_simple_for(self):
        self.assertRendered(
            '{% for _in=seq %}{{ item }} {% endfor %}',
            'a b c d e ',
            {'seq': 'abcde'},
        )

    def test_unpack_for(self):
        self.assertRendered(
            '{% for a, b, _in=seq %}{{ a }} == {{ b }},{% endfor %}',
            'a == 1,b == 2,',
            {'seq': (('a', 1), ('b', 2))}
        )
