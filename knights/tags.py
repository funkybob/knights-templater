
import ast

from .parser import wrap_name_in_context, visitor
from .library import Library

register = Library()


@register.tag
def load(parser, token):
    parser.load_library(token)


@register.tag
def extends(parser, token):
    from .loader import load_template
    parent = load_template(token)
    parser.parent = parent


@register.tag
def block(parser, token):
    name = token.strip()
    parser.build_method(name, endnodes=['endblock'])
    return ast.YieldFrom(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr=name,
                ctx=ast.Load()
            ),
            args=[
                ast.Name(id='context', ctx=ast.Load()),
            ],
            keywords=[], starargs=None, kwargs=None
        )
    )


@register.tag(name='if')
def do_if(parser, token):
    code = parser.parse_expression(token)

    nodelist, end = parser.parse_nodes_until('endif', 'else')

    if end == 'else':
        elsenodes, _ = parser.parse_nodes_until('endif')
    else:
        elsenodes = []

    return ast.If(test=code, body=nodelist, orelse=elsenodes)


def _create_with_scope(body, kwargs):
    '''
    Helper function to wrap a block in a scope stack:

    with ContextScope(context, **kwargs) as context:
        ... body ...
    '''
    return ast.With(
        items=[
            ast.withitem(
                context_expr=ast.Call(
                    func=ast.Name(id='ContextScope', ctx=ast.Load()),
                    args=[
                        ast.Name(id='context', ctx=ast.Load()),
                    ],
                    keywords=kwargs,
                    starargs=None, kwargs=None
                ),
                optional_vars=ast.Name(id='context', ctx=ast.Store())
            ),
        ],
        body=body,
    )


def _wrap_kwargs(kwargs):
    '''
    Ensure expressions in keyword arguments are wrapped.
    '''
    for kw in kwargs:
        visitor.visit(kw)
    return kwargs


@register.tag(name='for')
def do_for(parser, token):
    '''
    {% for a, b, c in iterable %}

    {% endfor %}

    We create the structure:

    for a, b, c in iterable:
        with ContextWrapper(context, a=a, b=b, c=c):
            ...
    '''
    code = ast.parse('for %s: pass' % token, mode='exec')

    loop = code.body[0]
    loop.iter = wrap_name_in_context(loop.iter)
    body, end = parser.parse_nodes_until('endfor', 'empty')

    if isinstance(loop.target, ast.Tuple):
        targets = [elt.id for elt in loop.target.elts]
    else:
        targets = [loop.target.id]

    kwargs = [
        ast.keyword(arg=elt, value=ast.Name(id=elt, ctx=ast.Load()))
        for elt in targets
    ]

    loop.body = [_create_with_scope(body, kwargs)]

    if end == 'empty':
        # Now we wrap our for block in:
        # if len(loop.iter):
        # else:
        empty, _ = parser.parse_nodes_until('endfor')

        loop = ast.If(
            test=ast.Call(
                func=ast.Name(id='len', ctx=ast.Load()),
                args=[loop.iter],
                keywords=[], starargs=None, kwargs=None
            ),
            body=[loop],
            orelse=empty
        )

    return loop


@register.tag(name='include')
def do_include(parser, token):
    from .loader import load_template

    args, kwargs = parser.parse_args(token)
    assert isinstance(args[0], ast.Str), "First argument to include tag must be a string"
    template_name = args[0].s
    tmpl = load_template(template_name)

    parser.helpers.setdefault('_includes', {})[template_name] = tmpl()

    action = ast.Yield(
        value=ast.Call(
            func=ast.Subscript(
                value=ast.Attribute(
                    value=ast.Name(id='helpers', ctx=ast.Load()),
                    attr='_includes',
                    ctx=ast.Load()
                ),
                slice=ast.Index(value=ast.Str(s=template_name)),
                ctx=ast.Load()
            ),
            args=[
                ast.Name(id='context', ctx=ast.Load()),
            ], keywords=[], starargs=None, kwargs=None
        )
    )

    if kwargs:
        kwargs = _wrap_kwargs(kwargs)
        return _create_with_scope([
            ast.Expr(value=action)
        ], kwargs)

    return action


@register.tag(name='with')
def do_with(parser, token):
    body, _ = parser.parse_nodes_until('endwith')

    args, kwargs = parser.parse_args(token)
    # Need to wrap name lookups in kwarg expressions
    kwargs = _wrap_kwargs(kwargs)
    action = _create_with_scope(body, kwargs)

    return action
