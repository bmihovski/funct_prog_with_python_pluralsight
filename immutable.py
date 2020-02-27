class Immutable(metaclass=abc.ABCMeta):
    __slots__ = ('__attrs__',)

    def __init__(self, *args, **kwargs):
        self.__attrs__ = frozenset()

    def __setattr__(self, name, value):
        if name == '__attrs__':
            return

        if name in self.__attrs__:
            raise AttributeError(f"Attempt to modify immutable attribute {name}")
        else:
            self.__attrs__ |= {name}

    def __delattr__(self, name):
        if name in self.__attrs__:
            raise AttributeError(f"Attempt to delete immutable attribute {name}")
        else:
            raise AttributeError(name)
