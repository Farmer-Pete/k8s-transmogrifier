from . import AbstractFilePlguin
from lib.decorators import classproperty


class JsonFilePlugin(AbstractFilePlguin):

    @classproperty
    def extension(cls):
        return '.json'

    def parse(self, content):
        import json
        return json.loads(content)

