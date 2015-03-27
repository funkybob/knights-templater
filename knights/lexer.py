from enum import Enum
import re

Token = Enum('Token', 'load comment text var block',)

tag_re = re.compile(
    '|'.join([
        r'{\!\s*(?P<load>.+?)\s*\!}',
        r'{%\s*(?P<tag>.+?)\s*%}',
        r'{{\s*(?P<var>.+?)\s*}}',
        r'{#\s*(?P<comment>.+?)\s*#}'
    ]),
    re.DOTALL
)


def tokenise(template):
    '''A generator which yields (type, content) pairs'''
    upto = 0
    # XXX Track line numbers and update nodes, so we can annotate the code
    for m in tag_re.finditer(template):
        start, end = m.span()
        if upto < start:
            yield (Token.text, template[upto:start])
        upto = end
        load, tag, var, comment = m.groups()
        if load is not None:
            yield (Token.load, load)
        elif tag is not None:
            yield (Token.block, tag)
        elif var is not None:
            yield (Token.var, var)
        else:
            yield (Token.comment, comment)
    if upto < len(template):
        yield (Token.text, template[upto:])
