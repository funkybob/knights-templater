from enum import Enum
import re

TokenType = Enum('Token', 'comment text var block',)


tag_re = re.compile(
    '|'.join([
        r'{%(-?)\s*(?P<block>.+?)\s*(-?)%}',
        r'{{(-?)\s*(?P<var>.+?)\s*(-?)}}',
        r'{#(-?)\s*(?P<comment>.+?)\s*(-?)#}'
    ]),
    re.DOTALL
)


class Token:
    __slots__ = ('mode', 'content', 'lineno')

    def __init__(self, mode, content, strip_mode, lineno=None):
        self.mode = mode
        self.content = content
        self.lineno = lineno
        self.strip_left = bool(strip_mode[0])
        self.strip_right = bool(strip_mode[1])


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

        # The middle value here is actually content
        lstrip, _, rstrip = m.groups()
        mode, content = list(m.groupsdict().items())[0]
        yield Token(TokenType[mode], content, (lstrip, rstrip), lineno)

    # if the last match ended before the end of the source, we have a tail Text
    # node.
    if upto < len(template):
        yield Token(TokenType.text, template[upto:], lineno)
