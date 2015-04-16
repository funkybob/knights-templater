from enum import Enum
import re

TokenType = Enum('Token', 'comment text var block',)


tag_re = re.compile(
    '|'.join([
        r'{%\s*(?P<block>.+?)\s*%}',
        r'{{\s*(?P<var>.+?)\s*}}',
        r'{#\s*(?P<comment>.+?)\s*#}'
    ]),
    re.DOTALL
)


class Token:
    __slots__ = ('mode', 'content', 'lineno')

    def __init__(self, mode, content, lineno=None):
        self.mode = mode
        self.content = content
        self.lineno = lineno


def tokenise(template):
    '''A generator which yields Token instances'''
    upto = 0
    lineno = 0

    for m in tag_re.finditer(template):

        start, end = m.span()
        lineno = template.count('\n', 0, start)
        # If there's a gap between our start and the end of the last match,
        # there's a Text node between.
        if upto < start:
            yield Token(TokenType.text, template[upto:start], lineno)
        upto = end

        mode = m.lastgroup
        content = m.group(m.lastgroup)
        yield Token(TokenType[mode], content, lineno)

    # if the last match ended before the end of the source, we have a tail Text
    # node.
    if upto < len(template):
        yield Token(TokenType.text, template[upto:], lineno)
