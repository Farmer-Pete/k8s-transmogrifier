from . import AbstractFilePlguin
from lib.decorators import classproperty


class PropertiesFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.properties'

    def parse(self, content):
        import configparser
        config = configparser.RawConfigParser()
        config.read_string('[root]\n' + content)
        return dict(config.items('root'))

