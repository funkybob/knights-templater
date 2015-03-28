import ast
from importlib import import_module

from .lexer import Token, tokenise


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

    state = {
        'bases': ['object'],
        'methods': [],
        'stream': tokenise(src),
        'tags': {},
    }

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

    state['methods'].append(func)

    state['methods'].append(build_method(state, '_root'))

    # define the class
    klass = ast.ClassDef(
        name='Template',
        bases=[
            ast.Name(id=base, ctx=ast.Load())
            for base in reversed(state['bases'])
        ],
        body=state['methods'],
        keywords=[],
        starargs=None,
        kwargs=None,
        decorator_list=[]
    )

    # Wrap it in a module
    inst = ast.Module(body=[klass])

    ast.fix_missing_locations(inst)

    # Compile code to create class
    code = compile(inst, filename='<compiler>', mode='exec')

    # Execute it and return the instance
    g = {}
    eval(code, g)

    return g['Template']


def build_method(state, name):

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

    # Parse Nodes
    # They need the parser, and state
    body.extend(parse_node(state))

    return func


class VarVisitor(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.Subscript(
            value=ast.Name(id='context', ctx=ast.Load()),
            slice=ast.Index(value=ast.Str(s=node.id)),
            ctx=ast.Load(),
        )


def parse_node(state):
    for mode, token in state['stream']:
        if mode == Token.load:
            load_library(state, token)
            continue
        elif mode == Token.text:
            node = ast.Yield(value=ast.Str(s=token))
        elif mode == Token.var:
            code = ast.parse(token, mode='eval')
            VarVisitor().visit(code)
            node = ast.Yield(value=code.body)
        elif mode == Token.block:
            #
            bits = token.strip().split(' ', 1)
            tag_name = bits.pop(0).strip()
            func = state['tags'][tag_name]
            node = func(state, *bits)
        else:
            # Must be a comment
            continue

        yield ast.Expr(value=node)


def load_library(state, path):
    '''
    Load a template library into the state.
    '''
    module = import_module(path)
    state['tags'].update(module.register.tags)
