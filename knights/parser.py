import ast
from importlib import import_module

from .lexer import TokenType, tokenise


def wrap_name_in_context(name):
    return ast.Subscript(
        value=ast.Name(id='context', ctx=ast.Load()),
        slice=ast.Index(value=ast.Str(s=name.id)),
        ctx=ast.Load(),
    )


class VarVisitor(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == '_':
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

    def build_method(self, name, endnodes=None):

        # body lead in
        body = [
            # _ = []
            ast.Assign(
                targets=[
                    ast.Name(id='_', ctx=ast.Store()),
                ],
                value=ast.List(elts=[], ctx=ast.Load())
            ),

            # _a = _.append
            ast.Assign(
                targets=[
                    ast.Name(id='_a', ctx=ast.Store()),
                ],
                value=ast.Attribute(
                    value=ast.Name(id='_', ctx=ast.Load()),
                    attr='append',
                    ctx=ast.Load()
                )
            ),

            # _e = _.extend
            ast.Assign(
                targets=[
                    ast.Name(id='_e', ctx=ast.Store()),
                ],
                value=ast.Attribute(
                    value=ast.Name(id='_', ctx=ast.Load()),
                    attr='extend',
                    ctx=ast.Load()
                )
            ),

        ]

        # Build the body
        if endnodes:
            _body, _ = self.parse_nodes_until(*endnodes)
        else:
           _body = list(self.parse_node())

        body.extend(_body)

        # Add return statement
        body.append(
            ast.Return(value=ast.Name(id='_', ctx=ast.Load())),
        )

        # Create the method
        func = ast.FunctionDef(
            name=name,
            args=ast.arguments(
                args=[
                    ast.arg(arg='self', annotation=None),
                    ast.arg(arg='context', annotation=None),
                ],
                vararg=None,
                kwonlyargs=[],
                kwarg=None,
                defaults=[],
                kw_defaults=[],
            ),
            body=body,
            decorator_list=[],
        )

        self.methods.append(func)

        return func

    def parse_node(self, endnodes=None):
        for token in self.stream:
            if token.mode == TokenType.text:
                node = value=ast.Call(
                    func=ast.Name(id='_a', ctx=ast.Load()),
                    args=[ast.Str(s=token.content)],
                    keywords=[], starargs=None, kwargs=None
                )

            elif token.mode == TokenType.var:
                code = self.parse_expression(token.content)
                node = value=ast.Call(
                    func=ast.Name(id='_a', ctx=ast.Load()),
                    args=[code],
                    keywords=[], starargs=None, kwargs=None
                )

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

            if isinstance(node, ast.Call):
                node = ast.Expr(value=node)

            yield node

    def parse_nodes_until(self, *endnodes):
        '''
        '''
        nodes = list(self.parse_node(endnodes=endnodes))
        end = nodes.pop()
        if not isinstance(end, str):
            raise SyntaxError('Did not find end node %e - found %r instead' % (endnodes, end))
        return nodes, end

    def build_class(self):
        return ast.ClassDef(
            name='Template',
            bases=[
                ast.Name(id='parent' if self.parent else 'object', ctx=ast.Load())
            ],
            body=self.methods,
            keywords=[],
            starargs=None,
            kwargs=None,
            decorator_list=[]
        )

    def parse_expression(self, expr):
        code = ast.parse(expr, mode='eval')
        visitor.visit(code)
        return code.body

    def parse_args(self, expr):
        code = ast.parse('x(%s)' % expr, mode='eval')

        return code.body.args, code.body.keywords
