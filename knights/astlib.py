from __future__ import unicode_literals

import ast
'''
Helpers for constructing AST in a less verbose manner.

In the majority of cases they allow for positional arguments, and provide
sane/common defaults
'''


def arguments(args=[], vararg=None, kwonlyargs=[], kwarg=None, defaults=[],
              kw_defaults=[]):

    return ast.arguments(args=args, vararg=vararg, kwonlyargs=kwonlyargs,
                         kwarg=kwarg, defaults=defaults,
                         kw_defaults=kw_defaults
                         )


def args(*names):
    return [
        ast.arg(arg=name, annotation=None)
        for name in names
    ]


def Attribute(value, attr, ctx=None):
    if ctx is None:
        ctx = ast.Load()

    return ast.Attribute(value=value, attr=attr, ctx=ctx)


def Name(id, ctx=None):
    if ctx is None:
        ctx = ast.Load()
    return ast.Name(id=id, ctx=ctx)


def Call(func, args=[], keywords=[], starargs=None, kwargs=None):

    return ast.Call(
        func=func,
        args=args,
        keywords=keywords,
        starargs=starargs,
        kwargs=kwargs
    )
