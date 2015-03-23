
from .library import Library

library = Library()


class Filter:
    '''
    Helper class for defining template filters.

    {{ value >> filter(arguments) }}
    '''
    def __rrshift__(self, other):
        pass


@library.register('title')
class TitleFilter(Filter):
    def __rshift__(self, other):
        return str(other).title()
