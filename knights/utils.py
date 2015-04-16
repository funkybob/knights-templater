
class Helpers:
    '''
    Provide a cheaper way to access helpers
    '''
    def __init__(self, members):
        for key, value in members.items():
            setattr(self, key, value)
