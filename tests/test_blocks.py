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
