import plugins.files

from lib.decorators import classproperty


class JsonFilePlugin(plugins.files.AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.json'

    def parse(self, content):
        import json
        return json.loads(content)

