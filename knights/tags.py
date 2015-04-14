
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

    # Need to inject the loop values back into the context
    # with ContextScope(context, ....) as context:
    inner = ast.With(
        items=[
            ast.withitem(
                context_expr=ast.Call(
                    func=ast.Name(id='ContextScope', ctx=ast.Load()),
                    args=[
                        ast.Name(id='context', ctx=ast.Load()),
                    ],
                    keywords=[
                        ast.keyword(arg=elt, value=ast.Name(id=elt, ctx=ast.Load()))
                        for elt in targets
                    ],
                    starargs=None, kwargs=None
                ),
                optional_vars=ast.Name(id='context', ctx=ast.Store())
            ),
        ],
        body=body,
    )

    loop.body = [inner]

    return loop


@register.tag(name='include')
def do_include(parser, token):
    from .loader import load_template
    template_name = token.strip()
    tmpl = load_template(template_name)

    parser.helpers.setdefault('_includes', {})[template_name] = tmpl()

    return ast.Expr(
        value=ast.Call(
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
    )
