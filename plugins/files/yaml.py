from . import AbstractFilePlguin
from lib.decorators import classproperty


try:
    from io import StringIO
except ImportError:
    # Fallback for python 2
    from SringIO import StringIO


class YamlFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.yaml'

    def parse(self, content):
        import yaml
        return yaml.safe_load(StringIO(content))

