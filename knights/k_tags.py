
import ast

from .klass import build_method
from .library import Library

register = Library()


def parse_args(bits):
    '''
    Parse tag bits as if they're function args
    '''
    code = ast.parse('x(%s)' % bits, mode='eval')
    return code.body.args, code.body.keywords


@register.tag(name='block')
def block(state, token):
    token = token.strip()
    func = build_method(state, token, endnode='endblock')
    state['methods'].append(func)
    return ast.YieldFrom(
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
    )
