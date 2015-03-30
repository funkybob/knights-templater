
import ast

from .parser import wrap_name_in_context
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
    {% for a, b, c in iterable %}

    {% endfor %}
    '''
    code = ast.parse('for %s: pass' % token, mode='exec')

    loop = code.body[0]
    loop.iter = wrap_name_in_context(loop.iter)
    loop.body = list(parser.parse_node(['endfor']))

    # Need to inject the loop values back into the context

    return loop
