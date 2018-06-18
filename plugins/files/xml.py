from __future__ import absolute_import

import unittest

from . import AbstractFilePlguin
from lib.decorators import classproperty


class XmlFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.xml'

    def parse(self, content):
        import xml.etree.ElementTree
        return xml.etree.ElementTree.fromstring(content)


class XmlFilePluginTest(unittest.TestCase):

    def test_parse(self):
        data_obj = [('key', 'value')]
        data_str = '<root key="value"/>'

        plugin = XmlFilePlugin()
        self.assertEqual(
            plugin.parse(data_str).items(),
            data_obj
        )

