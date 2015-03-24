
from .library import Library


register = Library()


@register.filter
def title(val):
    return str(val).title()
