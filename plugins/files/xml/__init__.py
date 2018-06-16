import plugins.files

from lib.decorators import classproperty


class XmlFilePlugin(plugins.files.AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.xml'

    def parse(self, content):
        import xml
        return xml.etree.ElementTree.fromstring(content)

