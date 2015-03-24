
from .library import Library
from .filters import Filter


register = Library()


@register.filter(name='title')
class TitleFilter(Filter):
    def __rshift__(self, other):
        return str(other).title()
