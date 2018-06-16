import plugins.files


class PropertiesFilePlugin(plugins.files.AbstractFilePlguin):

    @property
    def extension(self):
        return '.xml'

    def parse(self, content):
        import configparser
        config = configparser.RawConfigParser()
        config.read_string('[root]\n' + content)
        return dict(config.items('root'))

