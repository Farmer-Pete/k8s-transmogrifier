from __future__ import absolute_import

import unittest

from . import AbstractFilePlguin
from lib.decorators import classproperty


class JsonFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.json'

    def parse(self, content):
        import json
        return json.loads(content)


class JsonFilePluginTest(unittest.TestCase):

    def test_parse(self):
        data_obj = {'key': 'value'}
        data_str = '{"key": "value"}'

        plugin = JsonFilePlugin()
        self.assertEqual(plugin.parse(data_str), data_obj)

