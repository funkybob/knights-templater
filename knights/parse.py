
import ast
import re

tag_re = re.compile(
    '|'.join([
        r'{%\s*(?P<tag>.+?)\s*%}',
        r'{{\s*(?P<var>.+?)\s*}}',
        r'{#\s*(?P<comment>.+?)\s*#}'
    ]),
    re.DOTALL
)

TOKEN_TEXT = 0
TOKEN_VAR = 1
TOKEN_BLOCK = 2
TOKEN_COMMENT = 3
TOKEN_MAPPING = {
    TOKEN_TEXT: 'Text',
    TOKEN_VAR: 'Var',
    TOKEN_BLOCK: 'Block',
    TOKEN_COMMENT: 'Comment',
}


def tokenise(template):
    '''A generator which yields (type, content) pairs'''
    upto = 0
    # XXX Track line numbers and update nodes, so we can annotate the code
    for m in tag_re.finditer(template):
        start, end = m.span()
        if upto < start:
            yield (TOKEN_TEXT, template[upto:start])
        upto = end
        tag, var, comment = m.groups()
        if tag is not None:
            yield (TOKEN_BLOCK, tag)
        elif var is not None:
            yield (TOKEN_VAR, var)
        else:
            yield (TOKEN_COMMENT, comment)
    if upto < len(template):
        yield (TOKEN_TEXT, template[upto:])


class Node(object):
    def __init__(self, token, stream):
        self.token = token
        self.nodelist = []

    def render(self, context):
        return ''


class TextNode(Node):

    def render(self, context):
        return self.token


class VarNode(Node):
    def __init__(self, token, stream):
        super().__init__(token, stream)

        code = ast.parse(token, mode='eval')
        # XXX The magicks happen here

        self.code = compile(code, filename='<template>', mode='eval')

    def render(self, context):
        global_ctx = dict(context)
        return eval(self.code, global_ctx, {})


class BlockNode(Node):

    def __init__(self, token, stream):
        super().__init__(token, stream)

        code = ast.parse(token, mode='eval')
        assert isinstance(code.body, (ast.Tuple, ast.Name))


TOKEN_NODE = {
    TOKEN_TEXT: TextNode,
    TOKEN_VAR: VarNode,
    TOKEN_BLOCK: BlockNode,
    TOKEN_COMMENT: Node,
}


def parse(source):
    stream = tokenise(source)

    root = Node('', None)

    for mode, token in stream:
        node = TOKEN_NODE[mode](token, stream)
        if node:
            root.nodelist.append(node)

    return root
