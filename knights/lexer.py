from enum import Enum
import re

TokenType = Enum('Token', 'comment text var block',)


tag_re = re.compile(
    '|'.join([
        r'{%\s*(?P<tag>.+?)\s*%}',
        r'{{\s*(?P<var>.+?)\s*}}',
        r'{#\s*(?P<comment>.+?)\s*#}'
    ]),
    re.DOTALL
)


class Token:
    def __init__(self, mode, token, lineno=None):
        self.mode = mode
        self.token = token
        self.lineno = lineno


def tokenise(template):
    '''A generator which yields Token instances'''
    upto = 0
    lineno = 0
    # XXX Track line numbers and update nodes, so we can annotate the code
    for m in tag_re.finditer(template):
        start, end = m.span()
        lineno = template.count('\n', 0, start)
        if upto < start:
            yield Token(TokenType.text, template[upto:start], lineno)
        upto = end
        tag, var, comment = m.groups()
        if tag is not None:
            yield Token(TokenType.block, tag, lineno)
        elif var is not None:
            yield Token(TokenType.var, var, lineno)
        else:
            yield Token(TokenType.comment, comment, lineno)
    if upto < len(template):
        yield Token(TokenType.text, template[upto:], lineno)
