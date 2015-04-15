
import ast

from .parser import wrap_name_in_context
from .library import Library

register = Library()


@register.tag(name='load')
def load(parser, token):
    parser.load_library(token)


@register.tag(name='extends')
def extends(parser, token):
    from .loader import load_template
    parent = load_template(token)
    parser.parent = parent


@register.tag(name='block')
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

    nodelist = list(parser.parse_node(['endif']))

    return ast.If(test=code, body=nodelist, orelse=[])


@register.tag(name='else')
def do_else(parser, token=None):
    return ast.Yield(value=ast.Str(s=''))


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


@register.tag(name='for')
def do_for(parser, token):
    '''
    {% for a, b, c in iterable %}

    {% endfor %}

    We create the structure:

    for a, b, c in iterable:
        with helpers['forwrapper'](context, a=a, b=b, c=c):
            ...
    '''
    code = ast.parse('for %s: pass' % token, mode='exec')

    loop = code.body[0]
    loop.iter = wrap_name_in_context(loop.iter)
    body = list(parser.parse_node(['endfor']))

    if isinstance(loop.target, ast.Tuple):
        targets = [elt.id for elt in loop.target.elts]
    else:
        targets = [loop.target.id]

    kwargs = [
        ast.keyword(arg=elt, value=ast.Name(id=elt, ctx=ast.Load()))
        for elt in targets
    ]

    loop.body = [_create_with_scope(body, kwargs)]

    return loop


@register.tag(name='include')
def do_include(parser, token):
    from .loader import load_template

    args, kwargs = parser.parse_args(token)
    assert isinstance(args[0], ast.Str), "First argument to include tag must be a string"
    template_name = args[0].s
    tmpl = load_template(template_name)

    parser.helpers.setdefault('_includes', {})[template_name] = tmpl()

    action = ast.Call(
        func=ast.Subscript(
            value=ast.Subscript(
                value=ast.Name(id='helpers', ctx=ast.Load()),
                slice=ast.Index(value=ast.Str(s='_includes')),
                ctx=ast.Load()
            ),
            slice=ast.Index(value=ast.Str(s=template_name)),
            ctx=ast.Load()
        ),
        args=[
            ast.Name(id='context', ctx=ast.Load()),
        ], keywords=[], starargs=None, kwargs=None
    )

    if kwargs:
        return _create_with_scope([action], kwargs)

    return ast.Expr(value=action)


@register.tag(name='with')
def do_with(parser, token):
    body = list(parser.parse_node(['endfor']))

    args, kwargs = parser.parse_args(token)

    return _create_with_scope(body, kwargs)
