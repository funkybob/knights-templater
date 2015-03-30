import ast
from importlib import import_module

from .lexer import TokenType, tokenise


class VarVisitor(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.Subscript(
            value=ast.Name(id='context', ctx=ast.Load()),
            slice=ast.Index(value=ast.Str(s=node.id)),
            ctx=ast.Load(),
        )


class Parser:
    def __init__(self, src):
        self.stream = tokenise(src)
        self.bases = ['object']
        self.methods = []
        self.tags = {}

    def load_library(self, path):
        '''
        Load a template library into the state.
        '''
        module = import_module(path)
        self.tags.update(module.register.tags)

    def build_method(self, name, endnodes=None):

        # Define the body of the function
        body = [
            # Include a blank to ensure it's never empty
            ast.Expr(value=ast.Yield(value=ast.Str(s=''))),
        ]

        # Create the root method
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

        body.extend(self.parse_node(endnodes))

        self.methods.append(func)

        return func

    def parse_node(self, endnodes=None):
        for token in self.stream:
            if token.mode == TokenType.text:
                node = ast.Yield(value=ast.Str(s=token.token))
            elif token.mode == TokenType.var:
                code = self.parse_expression(token.token)
                node = ast.Yield(value=code)
            elif token.mode == TokenType.block:
                bits = token.token.strip().split(' ', 1)
                tag_name = bits.pop(0).strip()
                if endnodes and tag_name in endnodes:
                    return
                func = self.tags[tag_name]
                node = func(self, *bits)
            else:
                # Must be a comment
                continue

            if node is None:
                continue
            if isinstance(node, (ast.Yield, ast.YieldFrom)):
                node = ast.Expr(value=node, lineno=token.lineno)
            yield node

    def build_class(self):
        return ast.ClassDef(
            name='Template',
            bases=[
                ast.Name(id=base, ctx=ast.Load())
                for base in reversed(self.bases)
            ],
            body=self.methods,
            keywords=[],
            starargs=None,
            kwargs=None,
            decorator_list=[]
        )

    def parse_expression(self, expr):
        code = ast.parse(expr, mode='eval')
        VarVisitor().visit(code)
        return code.body


def kompile(src):
    '''
    Creates a new class based on the supplied template, and returnsit.

    class Template(object):
        def __call__(self, context):
            return ''.join(str(x) for x in self._root(context))

        def _root(self, context):
            yield ''
            yield ...
            yield from self.head(context)

    Blocks create new methods, and add a 'yield from self.{block}(context)' to
    the current function

    '''

    parser = Parser(src)
    parser.load_library('knights.k_tags')

    # Define the __call__ method
    func = ast.FunctionDef(
        name='__call__',
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
        body=[
            ast.Return(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Str(s=''),
                        attr='join',
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.GeneratorExp(
                            elt=ast.Call(
                                func=ast.Name(id='str', ctx=ast.Load()),
                                args=[
                                    ast.Name(id='x', ctx=ast.Load()),
                                ],
                                keywords=[], starargs=None, kwargs=None
                            ),
                            generators=[
                                ast.comprehension(
                                    target=ast.Name(id='x', ctx=ast.Store()),
                                    iter=ast.Call(
                                        func=ast.Attribute(
                                            value=ast.Name(id='self', ctx=ast.Load()),
                                            attr='_root',
                                            ctx=ast.Load()
                                        ),
                                        args=[
                                            ast.Name(id='context', ctx=ast.Load()),
                                        ], keywords=[], starargs=None, kwargs=None
                                    ),
                                    ifs=[]
                                ),
                            ]
                        ),
                    ],
                    keywords=[], starargs=None, kwargs=None
                )
            ),
        ],
        decorator_list=[],
    )

    parser.methods.append(func)
    parser.build_method('_root')

    klass = parser.build_class()

    # Wrap it in a module
    inst = ast.Module(body=[klass])

    ast.fix_missing_locations(inst)

    # Compile code to create class
    code = compile(inst, filename='<compiler>', mode='exec')

    # Execute it and return the instance
    g = {}
    eval(code, g)

    return g['Template']
