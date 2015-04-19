'''
Default helper functions
'''
from .escape import escape_html, escape_js
from .library import Library

register = Library()


@register.helper
def addslashes(value):
    return value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


@register.helper
def capfirst(value):
    return value and value[0].upper() + value[1:]


ESCAPES = {
    'html': escape_html,
    'js': escape_js,
}


@register.helper
def escape(value, mode='html'):
    return ESCAPES[mode](value)

register.helper(escape_html)
register.helper(escape_js)
