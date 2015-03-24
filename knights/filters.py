

class Filter:
    '''
    Helper class for defining template filters.

    {{ value >> filter(arguments) }}
    '''
    def __rrshift__(self, other):
        return other
