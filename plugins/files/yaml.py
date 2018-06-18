from __future__ import absolute_import

import unittest

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


class YamlFilePluginTest(unittest.TestCase):

    def test_parse(self):
        data_obj = {'key': 'value'}
        data_str = "key: value"

        plugin = YamlFilePlugin()
        self.assertEqual(plugin.parse(data_str), data_obj)

