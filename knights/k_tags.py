
import ast

from .library import Library

register = Library()


@register.tag(name='block')
def block(parser, token):
    token = token.strip()
    parser.build_method(token, endnodes=['endblock'])
    return ast.Expr(value=ast.YieldFrom(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr=token,
                ctx=ast.Load()
            ),
            args=[
                ast.Name(id='context', ctx=ast.Load()),
            ],
            keywords=[], starargs=None, kwargs=None
        )
    ))


@register.tag(name='if')
def do_if(parser, token):
    code = ast.parse(token, mode='eval')

    nodelist = list(parser.parse_node(['endif']))

    return ast.If(test=code.body, body=nodelist)


@register.tag(name='else')
def do_else(parser, token=None):
    return ast.Expr(value=ast.Yield(value=ast.Str(s='')))
