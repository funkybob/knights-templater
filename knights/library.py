from functools import partial

class Library(dict):

    def register(self, filt=None, name=None):
        if filt is None:
            return partial(self.register, name=name)

        if name is None:
            name = filt.__name__
        self[name] = filt
