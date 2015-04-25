from __future__ import unicode_literals

import sys
import ast
'''
Helpers for constructing AST in a less verbose manner.

In the majority of cases they allow for positional arguments, and provide
sane/common defaults
'''
PY2 = sys.version_info[0] == 2


def arguments(args=[], vararg=None, kwonlyargs=[], kwarg=None, defaults=[],
              kw_defaults=[]):

    return ast.arguments(args=args, vararg=vararg, kwonlyargs=kwonlyargs,
                         kwarg=kwarg, defaults=defaults,
                         kw_defaults=kw_defaults
                         )


def args(*names):
    if PY2:
        return [
            Name(name, ctx=ast.Param())
            for name in names
        ]
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
    return ast.Name(id=str(id), ctx=ctx)


def Call(func, args=[], keywords=[], starargs=None, kwargs=None):

    return ast.Call(
        func=func,
        args=args,
        keywords=keywords,
        starargs=starargs,
        kwargs=kwargs
    )


def With(context_expr, optional_vars=[], body=[]):
    if PY2:
        return ast.With(
            context_expr=context_expr,
            optional_vars=optional_vars,
            body=body,
        )

    return ast.With(
        items=[
            ast.withitem(
                context_expr=context_expr,
                optional_vars=optional_vars,
            ),
        ],
        body=body,
    )
