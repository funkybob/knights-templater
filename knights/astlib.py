import ast

"""
Helpers for constructing AST in a less verbose manner.

These are primarily to provide sane defaults (e.g. ctx=ast.Load())
"""


def Attribute(  # noqa: N802
    value: ast.Name,
    attr: str,
    ctx: ast.Load | ast.Store | ast.Del | None = None,
) -> ast.Attribute:
    if ctx is None:  # pragma: no cover
        ctx = ast.Load()

    return ast.Attribute(value=value, attr=attr, ctx=ctx)


def Name(  # noqa: N802
    id: str,  # noqa: A002
    ctx: ast.Load | ast.Store | ast.Del | None = None,
) -> ast.Name:
    if ctx is None:  # pragma: no cover
        ctx = ast.Load()
    return ast.Name(id=id, ctx=ctx)
