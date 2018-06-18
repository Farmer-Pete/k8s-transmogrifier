def walk(cls):

    for subclass in cls.__subclasses__():
        yield subclass

        for subsubclass in walk(subclass):
            yield subsubclass

