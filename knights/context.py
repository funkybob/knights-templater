from collections import defaultdict


class ContextScope(defaultdict):
    def __init__(self, parent, **kwargs):
        defaultdict.__init__(self, **kwargs)
        self.parent = parent

    def __missing__(self, key):
        return self.parent[key]

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass
