from .utils import TemplateTestCase


class CommentTagText(TemplateTestCase):

    def test_comment(self):
        self.assertRendered('{# test #}', '')
