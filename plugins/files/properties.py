import unittest

from . import AbstractFilePlguin
from lib.decorators import classproperty
from lib.py23 import unicode


class PropertiesFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.properties'

    def parse(self, content):
        import configparser
        config = configparser.RawConfigParser()
        config.read_string(unicode('[root]\n' + content))
        return dict(config.items('root'))


class PropertiesFilePluginTest(unittest.TestCase):

    def test_parse(self):
        data_obj = {'key': 'value'}
        data_str = "key=value"

        plugin = PropertiesFilePlugin()
        self.assertEqual(plugin.parse(data_str), data_obj)

