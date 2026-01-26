"""
Default helper functions
"""
from html import escape

from .escape import escape_js
from .library import Library

register = Library()

_slash_map = str.maketrans({
    '\\': r'\\',
    '"': r'\"',
    "'": r'\'',
})

@register.helper
def addslashes(value: str) -> str:
    return value.translate(_slash_map)


@register.helper
def capfirst(value: str) -> str:
    return value and value[0].upper() + value[1:]


ESCAPES = {
    'html': escape,
    'js': escape_js,
}


@register.helper
def escape(value: str, mode: str = 'html') -> str:
    return ESCAPES[mode](value)


register.helper(escape, name='escape_html')
register.helper(escape_js)
