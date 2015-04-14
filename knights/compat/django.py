import ast

from knights.library import Library

register = Library()


@register.tag
def static(parser, token):
    src = parser.parse_expression(token)
    return ast.Yield(value=ast.BinOp(
        left=ast.Str(s='/static/%s'),
        op=ast.Mod(),
        right=src,
    ))


@register.tag(name='include')
def do_include(parser, token):
    return ast.Yield(value=ast.Str(s='{include %s}' % token))


@register.helper
def safe(value):
    return str(value)
