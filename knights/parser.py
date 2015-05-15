import ast
from importlib import import_module

from . import astlib as _a
from .lexer import TokenType, tokenise


def wrap_name_in_context(name):
    return ast.Subscript(
        value=_a.Name('context'),
        slice=ast.Index(value=ast.Str(s=name.id)),
        ctx=ast.Load(),
    )


class VarVisitor(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id in ['_', 'self']:
            return node
        return wrap_name_in_context(node)

visitor = VarVisitor()


class Parser:
    def __init__(self, src):
        self.stream = tokenise(src)
        self.parent = None
        self.methods = []
        self.tags = {}
        self.helpers = {}

    def load_library(self, path):
        '''
        Load a template library into the state.
        '''
        module = import_module(path)
        self.tags.update(module.register.tags)
        self.helpers.update(module.register.helpers)

    def build_class(self):
        cls = ast.ClassDef(
            name='Template',
            bases=[
                _a.Name('parent' if self.parent else 'object')
            ],
            body=self.methods,
            keywords=[],
            starargs=None,
            kwargs=None,
            decorator_list=[]
        )

        cls.body.extend([

            # def _iterator(self, contetxt):
            #     return map(str, self._root(context))
            ast.FunctionDef(
                name='_iterator',
                args=_a.arguments(_a.args('self', 'context')),
                body=[
                    ast.Return(
                        value=_a.Call(_a.Name('map'), [
                            _a.Name('str'),
                            _a.Call(_a.Attribute(_a.Name('self'), '_root'), [
                                _a.Name('context'),
                            ]),
                        ])
                    )
                ],
                decorator_list=[],
            ),

            # def __call__(self, context):
            #     return ''.join(map(str, self._root(context)))
            ast.FunctionDef(
                name='__call__',
                args=_a.arguments(_a.args('self', 'context')),
                body=[
                    ast.Return(
                        value=_a.Call(
                            _a.Attribute(ast.Str(s=''), 'join'),
                            args=[
                                _a.Call(_a.Name('map'), [
                                    _a.Name('str'),
                                    _a.Call(
                                        _a.Attribute(_a.Name('self'), '_root'),
                                        [_a.Name('context')]
                                    ),
                                ]),
                            ],
                        )
                    ),
                ],
                decorator_list=[],
            ),

        ])

        return cls

    def build_method(self, name, endnodes=None):
        # Build the body
        if endnodes:
            body, _ = self.parse_nodes_until(*endnodes)
        else:
            body = list(self.parse_node())
        # If it's empty include a blank
        if not body:
            body.append(ast.Expr(value=ast.Yield(value=ast.Str(s=''))))

        # Create the method
        func = ast.FunctionDef(
            name=name,
            args=_a.arguments(_a.args('self', 'context')),
            body=body,
            decorator_list=[],
        )

        self.methods.append(func)

        return func

    def parse_node(self, endnodes=None):
        for token in self.stream:
            if token.mode == TokenType.text:
                node = ast.Yield(value=ast.Str(s=token.content))
            elif token.mode == TokenType.var:
                code = self.parse_expression(token.content)
                node = ast.Yield(value=code)
            elif token.mode == TokenType.block:
                bits = token.content.strip().split(' ', 1)
                tag_name = bits.pop(0).strip()
                if endnodes and tag_name in endnodes:
                    yield tag_name
                    return
                func = self.tags[tag_name]
                node = func(self, *bits)
            else:
                # Must be a comment
                continue

            if node is None:
                continue
            if isinstance(node, (ast.Yield, ast.YieldFrom)):
                node = ast.Expr(value=node)
            node.lineno = token.lineno
            yield node

    def parse_nodes_until(self, *endnodes):
        '''
        '''
        *nodes, end = list(self.parse_node(endnodes=endnodes))
        if end not in endnodes:
            raise SyntaxError('Did not find end node %r - found %r instead' % (
                endnodes, end
            ))
        return nodes, end

    def parse_expression(self, expr):
        code = ast.parse(expr, mode='eval')
        visitor.visit(code)
        return code.body

    def parse_args(self, expr):
        code = ast.parse('x(%s)' % expr, mode='eval')

        return code.body.args, code.body.keywords
