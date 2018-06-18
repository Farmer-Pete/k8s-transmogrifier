from __future__ import absolute_import
from . import AbstractFilePlguin
from lib.decorators import classproperty
from lib.py23 import StringIO, unicode


class YamlFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.yaml'

    def parse(self, content):
        import yaml
        return yaml.safe_load(StringIO(unicode(content)))

