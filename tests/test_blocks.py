from .utils import TemplateTestCase, Mock


class BlockTagTest(TemplateTestCase):

    def test_block_parse(self):
        self.assertRendered('{% now "%%" %}', '%')
