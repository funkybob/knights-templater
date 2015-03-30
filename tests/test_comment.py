from .utils import TemplateTestCase, Mock


class CommentTagText(TemplateTestCase):

    def test_comment(self):
        self.assertRendered('{# test #}', '')
