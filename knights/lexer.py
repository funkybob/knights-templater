import re
from enum import Enum

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

    def __repr__(self):
        return '<Token {}: "{:s}">'.format(self.mode.name, self.content)


def tokenise(template):
    '''A generator which yields Token instances'''
    upto = 0
    lineno = 0

    for m in tag_re.finditer(template):

        start, end = m.span()
        lineno = template.count('\n', 0, start) + 1  # Humans count from 1
        # If there's a gap between our start and the end of the last match,
        # there's a Text node between.
        if upto < start:
            yield Token(TokenType.text, template[upto:start], lineno)
        upto = end

        mode = m.lastgroup
        content = m.group(mode)
        yield Token(TokenType[mode], content, lineno)

    # if the last match ended before the end of the source, we have a tail Text
    # node.
    if upto < len(template):
        yield Token(TokenType.text, template[upto:], lineno)
