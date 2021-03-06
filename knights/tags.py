
import ast

from . import astlib as _a
from .library import Library
from .parser import visitor

register = Library()


@register.tag
def load(parser, token):
    args, kwargs = parser.parse_args(token)
    assert len(args) == 1, '"load" tag takes only one argument.'
    assert isinstance(args[0], ast.Str), \
        'First argument to "load" tag must be a string'

    parser.load_library(args[0].s)


@register.tag
def extends(parser, token):

    args, kwargs = parser.parse_args(token)
    assert len(args) == 1, '"extends" tag takes only one argument.'
    assert isinstance(args[0], ast.Str), \
        'First argument to "extends" tag must be a string'

    parent = parser.loader.load(args[0].s, raw=True)
    parser.parent = parent


@register.tag
def block(parser, token):
    name = token.strip()
    parser.build_method(name, endnodes=['endblock'])
    return ast.YieldFrom(
        value=_a.Call(_a.Attribute(_a.Name('self'), name), [
            _a.Name('context'),
        ])
    )


@register.tag(name='super')
def do_super(parser, token):
    '''
    Access the parent templates block.

    {% super name %}
    '''
    name = token.strip()
    return ast.YieldFrom(
        value=_a.Call(_a.Attribute(_a.Call(_a.Name('super')), name), [
            # _a.Attribute(_a.Name('context'), 'parent'),
            _a.Name('context'),
        ])
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
                context_expr=_a.Call(
                    _a.Name('ContextScope'),
                    [_a.Name('context')],
                    keywords=kwargs,
                ),
                optional_vars=_a.Name('context', ctx=ast.Store())
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

    with ContextWrapper(context) as context:
        for a, b, c in iterable:
            context.update(a=a, b=b, c=c)
            ...

    If there is a {% empty %} clause, we create:

    if iterable:
        { above code }
    else:
        { empty clause }
    '''
    code = ast.parse('for %s: pass' % token, mode='exec')

    # Grab the ast.For node
    loop = code.body[0]
    # Wrap its source iterable
    loop.iter = visitor.visit(loop.iter)

    # Get the body of the loop
    body, end = parser.parse_nodes_until('endfor', 'empty')

    # Build a list of target variable names
    if isinstance(loop.target, ast.Tuple):
        targets = [elt.id for elt in loop.target.elts]
    else:
        targets = [loop.target.id]

    kwargs = [
        ast.keyword(arg=elt, value=_a.Name(elt))
        for elt in targets
    ]

    # Insert our update call at the start of the loop body
    body.insert(0, ast.Expr(value=_a.Call(
        _a.Attribute(_a.Name('context'), 'update'),
        keywords=kwargs
    )))
    loop.body = body

    node = _create_with_scope([loop], [])

    if end == 'empty':
        # Now we wrap our for block in:
        # if loop.iter:
        # else:
        empty, _ = parser.parse_nodes_until('endfor')

        node = ast.If(
            test=loop.iter,
            body=[node],
            orelse=empty
        )

    return node


@register.tag(name='include')
def do_include(parser, token):
    args, kwargs = parser.parse_args(token)
    assert isinstance(args[0], ast.Str), \
        'First argument to "include" tag must be a string'
    template_name = args[0].s
    tmpl = parser.loader.load(template_name)

    parser.helpers.setdefault('_includes', {})[template_name] = tmpl

    # yield _._includes[name](context)
    action = ast.Yield(
        value=_a.Call(
            func=ast.Subscript(
                value=_a.Attribute(_a.Name('_'), '_includes'),
                slice=ast.Index(value=ast.Str(s=template_name)),
                ctx=ast.Load()
            ),
            args=[
                _a.Name('context'),
            ]
        )
    )

    if kwargs:
        kwargs = _wrap_kwargs(kwargs)
        return _create_with_scope([ast.Expr(value=action)], kwargs)

    return action


@register.tag(name='with')
def do_with(parser, token):
    body, _ = parser.parse_nodes_until('endwith')

    args, kwargs = parser.parse_args(token)
    # Need to wrap name lookups in kwarg expressions
    kwargs = _wrap_kwargs(kwargs)
    action = _create_with_scope(body, kwargs)

    return action


@register.tag
def macro(parser, token):
    '''
    Works just like block, but does not render.
    '''
    name = token.strip()
    parser.build_method(name, endnodes=['endmacro'])
    return ast.Yield(value=ast.Str(s=''))


@register.tag
def use(parser, token):
    '''
    Counterpart to `macro`, lets you render any block/macro in place.
    '''

    args, kwargs = parser.parse_args(token)
    assert isinstance(args[0], ast.Str), \
        'First argument to "include" tag must be a string'
    name = args[0].s

    action = ast.YieldFrom(
        value=_a.Call(_a.Attribute(_a.Name('self'), name), [
            _a.Name('context'),
        ])
    )

    if kwargs:
        kwargs = _wrap_kwargs(kwargs)
        return _create_with_scope([ast.Expr(value=action)], kwargs)

    return action
