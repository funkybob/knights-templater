from functools import partial


class Library:
    '''
    Container for registering tags and helpers
    '''
    def __init__(self):
        self.tags = {}
        self.helpers = {}

    def tag(self, func=None, name=None):
        if func is None:
            return partial(self.tag, name=name)

        if name is None:
            name = func.__name__

        self.tags[name] = func
        return func

    def helper(self, func=None, name=None):
        if func is None:
            return partial(self.helper, name=name)

        if name is None:
            name = func.__name__

        self.helpers[name] = func
        return func
