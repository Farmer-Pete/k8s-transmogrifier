class classproperty(property):
    # Source: https://stackoverflow.com/questions/128573/using-property-on-classmethods#39542816
    """
    Usage:

    >>> class Foo(object):
    >>>     _bar = 5
    >>>     @classproperty
    >>>     def bar(cls):
    >>>         return cls._bar
    >>>     @bar.setter
    >>>     def bar(cls, value):
    >>>         cls._bar = value
    >>>     @bar.deleter
    >>>     def bar(cls):
    >>>         del cls._bar
    """

    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))
