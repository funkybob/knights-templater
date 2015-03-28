import ast

from .lexer import Token, tokenise


def kompile(src):
    '''
    Defines a new class based on template tags, and returns an instance of it.

    class Template(object):
        def __call__(self, context):
            self.context = context
            yield from self._root(context)

        def _root(self, context):
            yield ''
            yield ...

    Blocks create new methods, and add a 'yield from self.{block}(context)' to
    the current function

    '''

    state = {
        'bases': ['object'],
        'methods': [],
        'stream': tokenise(src),
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
            ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(id='self', ctx=ast.Load()),
                        attr='context',
                        ctx=ast.Store()
                    ),
                ],
                value=ast.Name(id='context', ctx=ast.Load()),
            ),
            ast.Expr(value=ast.YieldFrom(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id='self', ctx=ast.Load()),
                        attr='_root',
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Name(id='context', ctx=ast.Load())
                    ],
                    keywords=[],
                    starargs=None,
                    kwargs=None,
                )
            )),
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

    inst = ast.Module(body=[
        klass,
        ast.Global(names=['inst']),
        ast.Assign(
            targets=[ast.Name(id='inst', ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id='Template', ctx=ast.Load()),
                args=[],
                keywords=[],
                starargs=None,
                kwargs=None
            ),
        )
    ])

    # Compile instanciating the klass
    ast.fix_missing_locations(inst)

    code = compile(inst, filename='<compiler>', mode='exec')

    # Execute it and return the instance
    g = {}
    eval(code, g)

    return g['inst']


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
    for node in parse_node(state):
        body.append(node)

    return func


def parse_node(state):
    for mode, token in state['stream']:
        if mode == Token.load:
            load_library(state, token)
            continue
        elif mode == Token.text:
            node = ast.Yield(value=ast.Str(s=token))
        elif mode == Token.var:
            code = ast.parse(token, mode='eval')
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


def load_library(state, token):
    '''
    Load a template library into the state.
    '''
    pass
