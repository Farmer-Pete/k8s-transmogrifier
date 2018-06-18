try:
    from io import StringIO
except ImportError:
    # Fallback for python 2
    from SringIO import StringIO

try:
    unicode = unicode
except NameError:
    # Implement unicode for backwards compatibility Python 3 -> 2
    unicode = str

