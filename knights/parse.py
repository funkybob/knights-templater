
import ast
from enum import Enum
from importlib import import_module
import re

tag_re = re.compile(
    '|'.join([
        r'{\!\s*(?P<load>.+?)\s*\!}',
        r'{%\s*(?P<tag>.+?)\s*%}',
        r'{{\s*(?P<var>.+?)\s*}}',
        r'{#\s*(?P<comment>.+?)\s*#}'
    ]),
    re.DOTALL
)


Token = Enum('Token', 'load comment text var block',)


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


class Node(object):
    def __init__(self, parser, token):
        self.token = token
        self.nodelist = []

    def __call__(self, context):
        return ''


class TextNode(Node):

    def __call__(self, context):
        return self.token


class NodeMangler(ast.NodeTransformer):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    def visit_BinOp(self, node):
        if not isinstance(node.op, ast.RShift):
            return node

        if isinstance(node.right, ast.Name) and node.right.id in self.parser.filters:
            # Turn "foo >> bar" into "_filter[bar](foo)"
            return ast.Call(
                func=ast.Subscript(
                    value=ast.Name(id='_filter', ctx=ast.Load()),
                    slice=ast.Index(value=ast.Str(s=node.right.id)),
                    ctx=ast.Load()
                ),
                args=[
                    node.left,
                ], keywords=[], starargs=None, kwargs=None
            )

        if isinstance(node.right, ast.Call) \
            and isinstance(node.right.func, ast.Name) \
            and node.right.func.id in self.parser.filters:
            # Turn "foo >> bar(baz..)" into "_filter[bar](foo, baz...)"
            return ast.Call(
                func=ast.Subscript(
                    value=ast.Name(id='_filter', ctx=ast.Load()),
                    slice=ast.Index(value=ast.Str(s=node.right.func.id)),
                    ctx=ast.Load()
                ),
                args=[node.left] + node.right.args,
                keywords=node.right.keywords,
                starargs=node.right.starargs,
                kwargs=node.right.kwargs,
            )
        return node


class VarNode(Node):
    def __init__(self, parser, token):
        super().__init__(parser, token)

        code = ast.parse(token, mode='eval')
        # XXX The magicks happen here
        code = NodeMangler(parser).visit(code)

        ast.fix_missing_locations(code)
        self.code = compile(code, filename='<template>', mode='eval')

    def __call__(self, context):
        return eval(self.code, context, {})


class BlockNode(Node):
    pass


class Parser:
    def __init__(self, source):
        self.stream = tokenise(source)
        self.libs = []
        self.tags = {}
        self.filters = {}
        self.load_library('knights.defaultfilters')
        self.load_library('knights.defaulttags')

    def __call__(self):

        nodelist = [
            node for node in self.parse_node()
        ]

        return nodelist

    def parse_node(self):
        for mode, token in self.stream:
            if mode == Token.load:
                self.load_library(token)
                continue
            elif mode == Token.text:
                node = TextNode(self, token)
            elif mode == Token.var:
                node = VarNode(self, token)
            elif mode == Token.block:
                # magicks go here
                bits = [x.strip() for x in token.strip().split(' ', 1)]
                tag_name = bits.pop(0)
                func = self.tags[tag_name]
                node = func(self, *bits)
            else:
                # Must be a comment
                continue

            yield node

    def load_library(self, path):
        '''
        Load a template library from the python path
        '''
        module = import_module(path)
        self.tags.update(module.register.tags)
        self.filters.update(module.register.filters)

    def parse_args(self, bits):
        '''
        Parse tag bits as if they're function args
        '''
        code = ast.parse('x(%s)' % bits, mode='eval')
        return code.body.args, code.body.keywords

    def resolve_args(self, context, args, kwargs):
        args = (
            compile(
                ast.fix_missing_locations(ast.Expression(body=arg)),
                filename='<tag>',
                mode='eval'
            )
            for arg in args
        )
        args = [eval(arg, context, {}) for arg in args]

        kwargs = compile(
            ast.fix_missing_locations(
                ast.Expression(
                    body=ast.Dict(
                        keys=[ast.Str(s=k.arg) for k in kwargs],
                        values=[k.value for k in kwargs],
                    )
                ),
            ),
            filename='<tag>',
            mode='eval'
        )
        kwargs = eval(kwargs, context, {})
        return args, kwargs
