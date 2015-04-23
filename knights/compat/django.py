import ast

from django.core.urlresolvers import reverse

import datetime

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


@register.helper
def capfirst(value):
    return value and value[0].upper() + value[1:]

@register.helper
def safe(value):
    return str(value)


@register.helper
def now(fmt):
    return datetime.datetime.now().strftime(fmt)

@register.helper
def url(name, *args, **kwargs):
    try:
        return reverse(name, args=args, kwargs=kwargs)
    except:
        return None
