import plugins.files


class XmlFilePlugin(plugins.files.AbstractFilePlguin):

    @property
    def extension(self):
        return '.xml'

    def parse(self, content):
        import xml
        return xml.etree.ElementTree.fromstring(content)

