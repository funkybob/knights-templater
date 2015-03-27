
import ast
from importlib import import_module

from .lexer import tokenise, Token


class Node(object):
    def __init__(self, parser, token=None):
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
        return list(self.parse_node())

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


def parse_args(bits):
    '''
    Parse tag bits as if they're function args
    '''
    code = ast.parse('x(%s)' % bits, mode='eval')
    return code.body.args, code.body.keywords


def resolve_args(context, args):
    args = (
        compile(
            ast.fix_missing_locations(ast.Expression(body=arg)),
            filename='<tag>',
            mode='eval'
        )
        for arg in args
    )
    return [eval(arg, context, {}) for arg in args]


def resolve_kwargs(context, kwargs):
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
    return eval(kwargs, context, {})


class BasicNode(Node):
    '''
    Helper class for building common-format template tags
    '''
    def __init__(self, parser, token=None):
        self.token = token
        self.args, self.kwargs = parse_args(token)

    def __call__(self, context):
        args = self.resolve_arguments(context)
        kwargs = self.resolve_keywords(context)
        return self.render(*args, **kwargs)

    def resolve_arguments(self, context):
        return resolve_args(context, self.args)

    def resolve_keywords(self, context):
        return resolve_kwargs(context, self.kwargs)
