import inspect


def not_implemented(cls):
    return (
        "Child class '%s' has not implemented required method or attribute: '%s'"
        % (cls.__name__, inspect.currentframe().f_back.f_code.co_name)
    )

