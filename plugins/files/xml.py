from . import AbstractFilePlguin
from lib.decorators import classproperty


class XmlFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.xml'

    def parse(self, content):
        import xml.etree.ElementTree
        return xml.etree.ElementTree.fromstring(content)

