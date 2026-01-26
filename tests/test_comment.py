from knights import render


class TestCommentTag:
    def test_comment(self):
        result = render('{# test #}')
        assert result == ''
