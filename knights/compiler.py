import ast

from .parser import Parser


def kompile(src, debug=False):
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
    parser.load_library('knights.tags')
    parser.load_library('knights.helpers')

    # Define the __call__ method
    # return ''.join(str(x) for x in self._root(context))
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

    if parser.parent:
        # Remove _root from the method list
        parser.methods = [
            method for method in parser.methods if method.name != '_root'
        ]
    klass = parser.build_class()

    # Wrap it in a module
    inst = ast.Module(body=[klass])

    ast.fix_missing_locations(inst)

    if debug:
        import astpp
        print(astpp.dump(inst))
    # Compile code to create class
    code = compile(inst, filename='<compiler>', mode='exec')

    # Execute it and return the instance
    g = {
        'helpers': parser.helpers,
        'parent': parser.parent,
    }
    eval(code, g)

    return g['Template']
