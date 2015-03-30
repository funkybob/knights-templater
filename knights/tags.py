
import ast

from .parser import VarVisitor
from .library import Library

register = Library()


@register.tag(name='load')
def load(parser, token):
    parser.load_library(token)


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
    {% for a, b, c, _in=iterable %}

    {% endfor %}
    '''
    args, kwargs = parser.parse_args(token)

    src = None
    for kw in kwargs:
        print(kw.arg, kw.value)
        if kw.arg == '_in':
            src = kw.value
            break
        raise ValueError('Only _in accepted as keyword in for tag.')

    for arg in args:
        VarVisitor().visit(arg)

    VarVisitor().visit(src)

    nodelist = list(parser.parse_node(['endfor']))

    return ast.For(target=args, iter=src, body=nodelist, orelse=[])
