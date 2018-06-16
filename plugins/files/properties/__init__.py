import plugins.files

from lib.decorators import classproperty


class PropertiesFilePlugin(plugins.files.AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.xml'

    def parse(self, content):
        import configparser
        config = configparser.RawConfigParser()
        config.read_string('[root]\n' + content)
        return dict(config.items('root'))

