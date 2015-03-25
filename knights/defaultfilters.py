
from .library import Library


register = Library()


@register.filter
def title(val):
    return str(val).title()


@register.filter
def add(val, more):
    return val + more
